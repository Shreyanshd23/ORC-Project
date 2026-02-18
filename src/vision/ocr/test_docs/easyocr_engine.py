from typing import List, Dict
import numpy as np


class LayoutClassifier:
    """
    Fast heuristic classifier (image-based)
    No PDF loading inside → faster pipeline
    """

    def __init__(self):
        pass

    def classify_images(self, images, start_page=1) -> List[Dict]:

        regions = []

        for i, img in enumerate(images):

            img_np = np.array(img)

            # grayscale
            gray = img_np.mean(axis=2)

            # -----------------------------
            # FEATURES
            # -----------------------------

            # horizontal variation (tables → low)
            horizontal_var = np.std(gray, axis=1).mean()

            # vertical variation (tables → structured)
            vertical_var = np.std(gray, axis=0).mean()

            # edge density (tables → more lines)
            edges = np.abs(np.diff(gray, axis=1)).mean()

            # -----------------------------
            # DECISION (IMPROVED)
            # -----------------------------
            if horizontal_var < 15 and edges > 5:
                label = "table"
            else:
                label = "text"

            regions.append({
                "page": start_page + i,
                "label": label
            })

        return regions
    


import easyocr
import numpy as np
import re
from metrics.accuracy import accuracy_report

# initialize once
reader = easyocr.Reader(['en'], gpu=False)


# -----------------------------
# OCR
# -----------------------------
def run_easyocr(image):

    # convert PIL → numpy
    image_np = np.array(image)

    results = reader.readtext(image_np)

    texts = []

    for (bbox, text, confidence) in results:
        # 🔥 filter low confidence
        if confidence > 0.5 and len(text.strip()) > 2:
            texts.append(text)

    return " ".join(texts)


# -----------------------------
# Preprocessing
# -----------------------------
def preprocess_text(text: str) -> str:
    text = text.lower()

    # remove weird chars but keep numbers
    text = re.sub(r"[^a-z0-9\s\.\-]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------
# Evaluation
# -----------------------------
def evaluate_text(gt_text: str, pred_text: str):

    return accuracy_report(
        preprocess_text(gt_text),
        preprocess_text(pred_text)
    )



import argparse
import json
from pathlib import Path

from pdf2image import convert_from_path

from engines.classifier import LayoutClassifier
from engines.text import run_easyocr, evaluate_text
from engines.table import run_table_pipeline


def normalize(text: str):
    return " ".join(text.lower().split())


def extract_gt_text(gt_json):
    texts = []

    def walk(obj):
        if isinstance(obj, dict):
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
        elif isinstance(obj, str):
            t = obj.strip()
            if t:
                texts.append(t)

    walk(gt_json)
    return "\n".join(texts)


def run_pipeline(dataset_dir: Path):

    classifier = LayoutClassifier()

    pdfs = list(dataset_dir.glob("*.pdf"))
    if not pdfs:
        print("❌ No PDFs found")
        return

    # -----------------------------
    # PAGE LIMITS
    # -----------------------------
    page_limits_file = dataset_dir / "page_limits.json"
    page_limits = {}

    if page_limits_file.exists():
        with open(page_limits_file, encoding="utf-8") as f:
            page_limits = json.load(f)

    # =============================
    # LOOP
    # =============================
    for pdf in pdfs:

        gt_path = dataset_dir / f"{pdf.stem}_gt.json"
        if not gt_path.exists():
            print(f"⚠ Skipping {pdf.name} (GT missing)")
            continue

        print("\n====================================")
        print(f"📄 {pdf.name}")
        print("====================================")

        with open(gt_path, encoding="utf-8") as f:
            gt_json = json.load(f)

        gt_text = extract_gt_text(gt_json)

        # -----------------------------
        # PAGE LIMITS
        # -----------------------------
        limits = page_limits.get(pdf.name, {})
        start_page = limits.get("start_page", 1)
        end_page = limits.get("end_page", None)

        # =============================
        # LOAD IMAGES FIRST (IMPORTANT)
        # =============================
        images = convert_from_path(
            str(pdf),
            dpi=120,
            first_page=start_page,
            last_page=end_page,
            poppler_path=r"C:\poppler\Library\bin"
        )

        # =============================
        # CLASSIFICATION (ON LIMITED IMAGES)
        # =============================
        print("\n🔍 Running Layout Classification...")

        regions = classifier.classify_images(images, start_page)

        text_regions = [r for r in regions if r["label"] == "text"]
        table_regions = [r for r in regions if r["label"] == "table"]

        print(f"Text Regions: {len(text_regions)}")
        print(f"Table Regions: {len(table_regions)}")

        # =============================
        # TEXT OCR
        # =============================
        print("\n--- TEXT OCR ---")

        text_output = ""

        # 🔥 LIMIT FOR SPEED (VERY IMPORTANT)
        text_regions = text_regions[:10]

        for region in text_regions:
            page_idx = region["page"] - start_page

            if 0 <= page_idx < len(images):
                image = images[page_idx]

                print(f"Processing page {region['page']}")

                extracted = run_easyocr(image)

                if len(extracted.strip()) > 5:
                    text_output += extracted + "\n"

        # fallback
        if not text_output.strip():
            print("⚠ No text detected, running fallback OCR...")
            for img in images[:5]:  # 🔥 limit fallback
                text_output += run_easyocr(img) + "\n"

        # =============================
        # TEXT METRICS
        # =============================
        text_metrics = evaluate_text(
            normalize(gt_text),
            normalize(text_output)
        )

        print(f"CER: {round(text_metrics['CER'],4)}")
        print(f"WER: {round(text_metrics['WER'],4)}")
        print(f"Char Accuracy: {round(text_metrics['Char_Accuracy'],4)}")

        # =============================
        # TABLE OCR (UNCHANGED ✅)
        # =============================
        print("\n--- TABLE OCR ---")

        table_result = run_table_pipeline(
            str(pdf),
            gt_json,
            start_page=start_page,
            end_page=end_page
        )

        fin = table_result["financial"]

        print(f"Numeric Accuracy: {fin.get('numeric_accuracy', 0)}")
        print(f"Line Item Accuracy: {fin.get('line_item_accuracy', 0)}")
        print(f"Section Accuracy: {fin.get('section_accuracy', 0)}")
        print(f"Disclosure Accuracy: {fin.get('disclosure_accuracy', 0)}")
        print(f"Financial Score: {fin.get('financial_overall_score', 0)}")

        # =============================
        # FINAL SCORE
        # =============================
        print("\n--- FINAL MERGED REPORT ---")

        final_score = (
            text_metrics["Char_Accuracy"] * 0.5 +
            fin.get("financial_overall_score", 0) * 0.5
        )

        print(f"Final Combined Score: {round(final_score,4)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Hybrid OCR Pipeline")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    run_pipeline(Path(args.dataset))
