import argparse
import json
from pathlib import Path
from pdf2image import convert_from_path

from engines.text import run_easyocr, evaluate_text
from engines.table import run_table_pipeline
from metrics.compliance_rules import validate_compliance


# -----------------------------
# HELPERS
# -----------------------------
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
            if obj.strip():
                texts.append(obj.strip())

    walk(gt_json)
    return "\n".join(texts)


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline(dataset_dir: Path):

    pdfs = list(dataset_dir.glob("*.pdf"))

    page_limits = {}
    limits_file = dataset_dir / "page_limits.json"

    if limits_file.exists():
        page_limits = json.load(open(limits_file))

    for pdf in pdfs:

        print("\n====================================")
        print(f"📄 {pdf.name}")
        print("====================================")

        gt_path = dataset_dir / f"{pdf.stem}_gt.json"
        if not gt_path.exists():
            print("⚠ GT missing, skipping")
            continue

        gt_json = json.load(open(gt_path))
        gt_text = extract_gt_text(gt_json)

        # -----------------------------
        # PAGE LIMITS
        # -----------------------------
        limits = page_limits.get(pdf.name, {})
        start_page = limits.get("start_page", 1)
        end_page = limits.get("end_page")

        # =============================
        # TEXT PIPELINE (EasyOCR)
        # =============================
        print("\n--- TEXT OCR (EasyOCR) ---")

        images = convert_from_path(
            str(pdf),
            dpi=120,
            first_page=start_page,
            last_page=end_page,
            poppler_path=r"C:\poppler\Library\bin"
        )

        text_output = ""

        for i, img in enumerate(images):
            print(f"Processing page {start_page + i}")
            out = run_easyocr(img)

            if len(out.strip()) > 5:
                text_output += out + "\n"

        text_metrics = evaluate_text(
            normalize(gt_text),
            normalize(text_output)
        )

        print(f"CER: {round(text_metrics['CER'],4)}")
        print(f"WER: {round(text_metrics['WER'],4)}")
        print(f"Char Accuracy: {round(text_metrics['Char_Accuracy'],4)}")

        # =============================
        # TABLE PIPELINE (Docling)
        # =============================
        print("\n--- TABLE OCR (Docling) ---")

        table = run_table_pipeline(
            str(pdf),
            gt_json,
            start_page=start_page,
            end_page=end_page
        )

        fin = table["financial"]

        print(f"Numeric Accuracy: {fin.get('numeric_accuracy', 0)}")
        print(f"Row Accuracy: {fin.get('row_accuracy', 0)}")
        print(f"Header Accuracy: {fin.get('header_accuracy', 0)}")
        print(f"Column Accuracy: {fin.get('column_accuracy', 0)}")
        print(f"Financial Score: {fin.get('financial_overall_score', 0)}")

        # =============================
        # COMPLIANCE CHECK
        # =============================
        print("\n--- COMPLIANCE ---")

        compliance = validate_compliance(gt_json, table["text"])

        for rule in compliance:
            print(f"{rule['rule']}: {rule['status']}")

        # =============================
        # FINAL SCORE
        # =============================
        final_score = (
            text_metrics["Char_Accuracy"] * 0.4 +
            fin.get("financial_overall_score", 0) * 0.6
        )

        print("\n--- FINAL ---")
        print(f"Final Score: {round(final_score,4)}")


# =============================
# ENTRY
# =============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Dual OCR Pipeline")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    run_pipeline(Path(args.dataset))
