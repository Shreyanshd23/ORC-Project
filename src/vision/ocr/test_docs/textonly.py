from typing import List, Dict
import numpy as np
import easyocr
import re
import argparse
import json
from pathlib import Path
from pdf2image import convert_from_path

from metrics.accuracy import accuracy_report


# =========================================================
# CLASSIFIER (NO IMPORT — DEFINED HERE)
# =========================================================
class LayoutClassifier:
    """
    Fast heuristic classifier (image-based)
    """

    def classify_images(self, images, start_page=1) -> List[Dict]:

        regions = []

        for i, img in enumerate(images):

            img_np = np.array(img)

            # grayscale
            gray = img_np.mean(axis=2)

            # FEATURES
            horizontal_var = np.std(gray, axis=1).mean()
            vertical_var = np.std(gray, axis=0).mean()
            edges = np.abs(np.diff(gray, axis=1)).mean()

            # DECISION
            if horizontal_var < 15 and edges > 5:
                label = "table"
            else:
                label = "text"

            regions.append({
                "page": start_page + i,
                "label": label
            })

        return regions


# =========================================================
# OCR
# =========================================================
reader = easyocr.Reader(['en'], gpu=False)


def run_easyocr(image):
    image_np = np.array(image)
    results = reader.readtext(image_np)

    texts = []

    for (bbox, text, confidence) in results:
        if confidence > 0.5 and len(text.strip()) > 2:
            texts.append(text)

    return " ".join(texts)


# =========================================================
# PREPROCESS
# =========================================================
def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================================================
# EVALUATION
# =========================================================
def evaluate_text(gt_text: str, pred_text: str):
    return accuracy_report(
        preprocess_text(gt_text),
        preprocess_text(pred_text)
    )


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

def save_outputs(pdf_name: str, page_outputs: List[Dict], output_dir: Path):
    
    output_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # JSON
    # -------------------------
    json_path = output_dir / f"{pdf_name}.json"

    json_data = {
        "document": pdf_name,
        "pages": page_outputs
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    # -------------------------
    # MARKDOWN
    # -------------------------
    md_path = output_dir / f"{pdf_name}.md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {pdf_name}\n\n")

        for page in page_outputs:
            f.write(f"## Page {page['page']}\n")
            for block in page["blocks"]:
                if block["type"] == "heading":
                    f.write(f"### {block['text']}\n\n")
                else:
                    f.write(block["text"] + "\n\n")


    print(f"📁 Saved: {json_path.name}, {md_path.name}")
def classify_line(line: str) -> str:
    line = line.strip()

    if not line:
        return "empty"

    # heading rules
    if (
        line.isupper()
        or (len(line.split()) <= 6 and not line.endswith("."))
        or any(k in line.lower() for k in [
            "balance sheet",
            "statement",
            "cash flow",
            "notes",
            "summary"
        ])
    ):
        return "heading"

    # numeric-heavy (tables / financial)
    digits = sum(c.isdigit() for c in line)
    if digits > len(line) * 0.3:
        return "numeric"

    return "paragraph"

# =========================================================
# MAIN PIPELINE
# =========================================================
def run_pipeline(dataset_dir: Path):

    classifier = LayoutClassifier()

    pdfs = list(dataset_dir.glob("*.pdf"))
    if not pdfs:
        print("❌ No PDFs found")
        return

    # PAGE LIMITS
    page_limits_file = dataset_dir / "page_limits.json"
    page_limits = {}

    if page_limits_file.exists():
        with open(page_limits_file, encoding="utf-8") as f:
            page_limits = json.load(f)

    # LOOP
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

        # PAGE LIMITS
        limits = page_limits.get(pdf.name, {})
        start_page = limits.get("start_page", 1)
        end_page = limits.get("end_page", None)

        # LOAD IMAGES
        images = convert_from_path(
            str(pdf),
            dpi=120,
            first_page=start_page,
            last_page=end_page,
            poppler_path=r"C:\poppler\Library\bin"  # adjust if needed
        )

        # CLASSIFICATION
        print("\n🔍 Running Layout Classification...")
        regions = classifier.classify_images(images, start_page)

        text_regions = [r for r in regions if r["label"] == "text"]

        print(f"Text Regions: {len(text_regions)}")

        # TEXT OCR
        print("\n--- TEXT OCR ---")

        text_output = ""
        page_outputs = []

        # limit for speed
        text_regions = text_regions[:10]

        for region in text_regions:
            page_idx = region["page"] - start_page

            if 0 <= page_idx < len(images):
                image = images[page_idx]

                print(f"Processing page {region['page']}")

                extracted = run_easyocr(image)

                if len(extracted.strip()) > 5:
                    text_output += extracted + "\n"

                    lines = extracted.split("\n")

                    blocks = []

                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue

                        blocks.append({
                            "type": classify_line(line),
                            "text": line
                        })

                    page_outputs.append({
                        "page": region["page"],
                        "blocks": blocks
                    })


        # fallback
        if not text_output.strip():
            print("⚠ No text detected, running fallback OCR...")
            for i, img in enumerate(images[:5]):
                extracted = run_easyocr(img)

                text_output += extracted + "\n"

                page_outputs.append({
                    "page": start_page + i,
                    "text": extracted
                })

        # SAVE OUTPUTS
        output_dir = dataset_dir / "outputs"
        save_outputs(pdf.stem, page_outputs, output_dir)

        # METRICS
        text_metrics = evaluate_text(
            normalize(gt_text),
            normalize(text_output)
        )

        print(f"CER: {round(text_metrics['CER'],4)}")
        print(f"WER: {round(text_metrics['WER'],4)}")


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Hybrid OCR Pipeline")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    run_pipeline(Path(args.dataset))
