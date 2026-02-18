import argparse
import json
from pathlib import Path

from engines.classifier import LayoutClassifier
from engines.text import run_paddle_ocr, evaluate_text
from engines.table import run_table_ocr, evaluate_table

import fitz  # PyMuPDF


# ============================================================
# HELPERS
# ============================================================

def normalize(text: str) -> str:
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


def pdf_to_image(pdf_path, page_num=0):
    doc = fitz.open(pdf_path)
    pix = doc[page_num].get_pixmap()
    img_path = f"temp_page_{page_num}.png"
    pix.save(img_path)
    return img_path


# ============================================================
# MAIN BENCHMARK
# ============================================================

def run_benchmark(dataset_dir: Path):

    classifier = LayoutClassifier()

    pdfs = list(dataset_dir.glob("*.pdf"))
    if not pdfs:
        print("❌ No PDFs found")
        return

    page_limits_file = dataset_dir / "page_limits.json"
    page_limits = {}

    if page_limits_file.exists():
        with open(page_limits_file, encoding="utf-8") as f:
            page_limits = json.load(f)

    total_pages = 0
    total_time = 0
    cer_sum = 0
    wer_sum = 0
    char_acc_sum = 0
    fin_sum = 0
    doc_count = 0

    per_doc_results = []

    for pdf in pdfs:

        gt_path = dataset_dir / f"{pdf.stem}_gt.json"
        if not gt_path.exists():
            print(f"⚠ Skipping {pdf.name} (GT missing)")
            continue

        print("\n====================================")
        print(f"📄 {pdf.name}")
        print("====================================")

        limits = page_limits.get(pdf.name, {})
        start_page = limits.get("start_page", 1)
        end_page = limits.get("end_page", 1)

        with open(gt_path, encoding="utf-8") as f:
            gt_json = json.load(f)

        gt_text = extract_gt_text(gt_json)

        # =====================================================
        # PROCESS EACH PAGE
        # =====================================================
        full_text_output = ""
        full_table_markdown = ""

        pages_processed = 0

        for page_num in range(start_page - 1, end_page):

            image_path = pdf_to_image(str(pdf), page_num)

            regions = classifier.classify(image_path)

            for region in regions:

                # -----------------------------
                # TEXT REGION → PaddleOCR
                # -----------------------------
                if region["type"] == "text":
                    text = run_paddle_ocr(image_path)
                    full_text_output += text + "\n"

                # -----------------------------
                # TABLE REGION → Docling
                # -----------------------------
                elif region["type"] == "table":
                    table_result = run_table_ocr(
                        str(pdf),
                        start_page=page_num + 1,
                        end_page=page_num + 1
                    )

                    if table_result["success"]:
                        full_table_markdown += table_result["markdown"] + "\n"

            pages_processed += 1

        # =====================================================
        # TEXT EVALUATION (CER/WER)
        # =====================================================
        text_metrics = evaluate_text(
            gt_text,
            full_text_output
        )

        print("\n--- Technical OCR (TEXT) ---")
        print(f"CER: {round(text_metrics['CER'],4)}")
        print(f"WER: {round(text_metrics['WER'],4)}")
        print(f"Char Accuracy: {round(text_metrics['Char_Accuracy'],4)}")

        # =====================================================
        # TABLE EVALUATION (FINANCIAL)
        # =====================================================
        table_metrics = evaluate_table(
            gt_json,
            {"markdown": full_table_markdown}
        )

        print("\n--- Financial (TABLE) ---")
        print(f"Numeric Accuracy: {table_metrics.get('numeric_accuracy', 0)}")
        print(f"Line Item Accuracy: {table_metrics.get('line_item_accuracy', 0)}")
        print(f"Section Accuracy: {table_metrics.get('section_accuracy', 0)}")
        print(f"Disclosure Accuracy: {table_metrics.get('disclosure_accuracy', 0)}")
        print(f"Financial Overall Score: {table_metrics.get('financial_overall_score', 0)}")

        # =====================================================
        # AGGREGATION
        # =====================================================
        doc_count += 1
        total_pages += pages_processed

        cer_sum += text_metrics["CER"] * pages_processed
        wer_sum += text_metrics["WER"] * pages_processed
        char_acc_sum += text_metrics["Char_Accuracy"] * pages_processed
        fin_sum += table_metrics.get("financial_overall_score", 0)

        per_doc_results.append({
            "pdf": pdf.name,
            "CER": text_metrics["CER"],
            "WER": text_metrics["WER"],
            "Char_Accuracy": text_metrics["Char_Accuracy"],
            "Financial_Score": table_metrics.get("financial_overall_score", 0)
        })

    if doc_count == 0:
        print("No documents processed.")
        return

    final_summary = {
        "documents_processed": doc_count,
        "total_pages": total_pages,
        "average_CER": round(cer_sum / total_pages, 4),
        "average_WER": round(wer_sum / total_pages, 4),
        "average_character_accuracy": round(char_acc_sum / total_pages, 4),
        "average_financial_score": round(fin_sum / doc_count, 4),
    }

    print("\n==============================")
    print("📊 FINAL SUMMARY")
    print("==============================")
    print(json.dumps(final_summary, indent=2))

    output_path = dataset_dir / "benchmark_full_report.json"
    output_path.write_text(
        json.dumps({
            "per_document_results": per_doc_results,
            "final_summary": final_summary
        }, indent=2),
        encoding="utf-8"
    )

    print(f"\n📁 {output_path.name} saved")


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Hybrid OCR Benchmark Runner")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    run_benchmark(Path(args.dataset))
