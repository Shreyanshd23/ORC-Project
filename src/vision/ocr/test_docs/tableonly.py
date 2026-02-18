import re
import time
import json
import argparse
import logging
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

import numpy as np

from PyPDF2 import PdfReader, PdfWriter

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# SIMPLE OCR METRICS (REPLACEMENT)
# ============================================================
def accuracy_report(gt: str, pred: str):
    gt_words = gt.split()
    pred_words = pred.split()

    common = sum(1 for w in gt_words if w in pred_words)

    wer = 1 - (common / len(gt_words)) if gt_words else 0
    cer = wer  # simplified
    char_acc = 1 - cer

    return {
        "CER": cer,
        "WER": wer,
        "Char_Accuracy": char_acc
    }

# ============================================================
# FINANCIAL METRICS
# ============================================================
def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())

def normalize_number(n: str) -> str:
    return re.sub(r"[^\d\.-]", "", n)

def extract_all_numbers(obj: Any) -> List[str]:
    numbers = []
    if isinstance(obj, dict):
        for v in obj.values():
            numbers.extend(extract_all_numbers(v))
    elif isinstance(obj, list):
        for item in obj:
            numbers.extend(extract_all_numbers(item))
    elif isinstance(obj, str):
        numbers.extend(re.findall(r"-?\d[\d,\.]*", obj))
    elif isinstance(obj, (int, float)):
        numbers.append(str(obj))
    return numbers

def extract_all_text(obj: Any) -> List[str]:
    texts = []
    if isinstance(obj, dict):
        for v in obj.values():
            texts.extend(extract_all_text(v))
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_all_text(item))
    elif isinstance(obj, str):
        if obj.strip():
            texts.append(obj.strip())
    return texts

def financial_accuracy_report(gt_json, ocr_text):

    normalized_ocr = normalize_text(ocr_text)
    normalized_ocr_numbers = normalize_number(ocr_text)

    gt_numbers = [normalize_number(n) for n in extract_all_numbers(gt_json) if normalize_number(n)]
    matched_numbers = sum(1 for n in gt_numbers if n in normalized_ocr_numbers)

    numeric_accuracy = matched_numbers / len(gt_numbers) if gt_numbers else 0

    gt_texts = [normalize_text(t) for t in extract_all_text(gt_json) if len(t) > 3]
    matched_items = sum(1 for t in gt_texts if t in normalized_ocr)

    line_item_accuracy = matched_items / len(gt_texts) if gt_texts else 0

    sections = ["balance sheet", "profit", "cash flow", "auditor"]
    section_accuracy = sum(1 for s in sections if s in normalized_ocr) / len(sections)

    disclosures = ["true and fair", "earnings", "march"]
    disclosure_accuracy = sum(1 for d in disclosures if d in normalized_ocr) / len(disclosures)

    final_score = (
        numeric_accuracy * 0.4 +
        line_item_accuracy * 0.2 +
        section_accuracy * 0.2 +
        disclosure_accuracy * 0.2
    )

    return {
        "financial_overall_score": round(final_score, 4)
    }

# ============================================================
# COMPLIANCE
# ============================================================
def validate_compliance(gt_json, ocr_text):

    text_lower = ocr_text.lower()
    results = []

    sections = ["balance sheet", "profit", "cash flow", "auditor"]

    for s in sections:
        results.append({
            "rule": s,
            "status": "PASS" if s in text_lower else "FAIL"
        })

    return results

# ============================================================
# OCR ENGINE (SIMPLIFIED DOC OCR)
# ============================================================
class OCREngine:

    def __init__(self):
        logger.info("OCR Engine initialized")
        self.reader = easyocr.Reader(['en'], gpu=False)

    def process_pdf(self, pdf_path: str):

        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        return {
            "success": True,
            "text": text,
            "pages": len(reader.pages),
            "time_sec": 1
        }

# ============================================================
# HELPER
# ============================================================
def normalize(text: str):
    return " ".join(text.lower().split())

def extract_gt_text(gt_json):
    return "\n".join(extract_all_text(gt_json))

# ============================================================
# MAIN BENCHMARK
# ============================================================
def run_benchmark(dataset_dir: Path):

    engine = OCREngine()

    pdfs = list(dataset_dir.glob("*.pdf"))

    for pdf in pdfs:

        gt_path = dataset_dir / f"{pdf.stem}_gt.json"
        if not gt_path.exists():
            continue

        print(f"\n📄 {pdf.name}")

        result = engine.process_pdf(str(pdf))

        gt_json = json.loads(gt_path.read_text())
        gt_text = extract_gt_text(gt_json)

        ocr_metrics = accuracy_report(
            normalize(gt_text),
            normalize(result["text"])
        )

        fin_metrics = financial_accuracy_report(gt_json, result["text"])

        print(f"CER: {ocr_metrics['CER']}")
        print(f"Financial Score: {fin_metrics['financial_overall_score']}")

# ============================================================
# ENTRY
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    run_benchmark(Path(args.dataset))
