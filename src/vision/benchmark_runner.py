import argparse
import json
from pathlib import Path
from structure_builder import build_gt_like_json

from engines.docling_engine import OCREngine
from metrics.accuracy import accuracy_report
from metrics.accuracy_financial_new import financial_accuracy_report
from metrics.compliance_rules import validate_compliance


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


# ✅ FIXED F1 (STRUCTURE vs STRUCTURE)
def compute_f1(gt_json, pred_json):

    def extract_entities(obj):
        entities = []

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (str, int, float)):
                    entities.append((str(k).lower(), str(v).lower()))
                else:
                    entities.extend(extract_entities(v))

        elif isinstance(obj, list):
            for item in obj:
                entities.extend(extract_entities(item))

        return entities

    gt_entities = set(extract_entities(gt_json))
    pred_entities = set(extract_entities(pred_json))

    tp = len(gt_entities & pred_entities)

    precision = tp / len(pred_entities) if pred_entities else 0
    recall = tp / len(gt_entities) if gt_entities else 0

    if precision + recall == 0:
        return 0, 0, 0

    f1 = 2 * precision * recall / (precision + recall)

    return round(f1, 4), round(precision, 4), round(recall, 4)


# ✅ KEEP (simple token overlap)
def compute_extraction_accuracy(gt_json, pred_text):
    gt_str = json.dumps(gt_json).lower()
    pred_text = pred_text.lower()

    total = len(gt_str.split())
    correct = sum(1 for t in gt_str.split() if t in pred_text)

    return round(correct / total, 4) if total else 0


def run_benchmark(dataset_dir: Path):

    engine = OCREngine()

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
    f1_sum = 0
    extraction_sum = 0

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
        start_page = limits.get("start_page")
        end_page = limits.get("end_page")

        result = engine.process_pdf(
            str(pdf),
            start_page=start_page,
            end_page=end_page,
        )

        if not result["success"]:
            print("❌ OCR failed")
            continue

        with open(gt_path, encoding="utf-8") as f:
            gt_json = json.load(f)

        gt_text = extract_gt_text(gt_json)

        # -----------------------------
        # OCR Metrics
        # -----------------------------
        ocr_metrics = accuracy_report(
            normalize(gt_text),
            normalize(result["text"])
        )

        print("\n--- Technical OCR ---")
        print(f"CER: {round(ocr_metrics['CER'],4)}")
        print(f"WER: {round(ocr_metrics['WER'],4)}")
        print(f"Char Accuracy: {round(ocr_metrics['Char_Accuracy'],4)}")

        # -----------------------------
        # Financial Metrics
        # -----------------------------
        fin_metrics = financial_accuracy_report(
            gt_json,
            result["text"]
        )

        print("\n--- Financial ---")
        print(f"Numeric Accuracy: {fin_metrics['numeric_accuracy']}")
        print(f"Line Item Accuracy: {fin_metrics['line_item_accuracy']}")
        print(f"Section Accuracy: {fin_metrics['section_accuracy']}")
        print(f"Disclosure Accuracy: {fin_metrics['disclosure_accuracy']}")
        print(f"\nFinancial Overall Score: {fin_metrics['financial_overall_score']}")

        # -----------------------------
        # ✅ STRUCTURED OUTPUT FIRST
        # -----------------------------
        structured_output = build_gt_like_json(result)
        structured_output["pdf"] = pdf.name

        # -----------------------------
        # ✅ F1 (FIXED)
        # -----------------------------
        f1, precision, recall = compute_f1(gt_json, structured_output)

        print("\n--- Key Information Extraction ---")
        print(f"F1 Score: {f1}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")

        # -----------------------------
        # Extraction Accuracy
        # -----------------------------
        extraction_acc = compute_extraction_accuracy(gt_json, result["text"])

        print("\n--- Extraction Accuracy ---")
        print(f"Extraction Accuracy: {extraction_acc}")

        # -----------------------------
        # Compliance
        # -----------------------------
        print("\n--- Compliance ---")
        compliance_results = validate_compliance(gt_json, result["text"])
        for rule in compliance_results:
            print(f"{rule['rule']}: {rule['status']}")

        # -----------------------------
        # SAVE OUTPUT
        # -----------------------------
        output_json_path = dataset_dir / f"{pdf.stem}_output.json"
        output_json_path.write_text(
            json.dumps(structured_output, indent=2),
            encoding="utf-8"
        )

        print(f"📁 Saved → {output_json_path.name}")

        # -----------------------------
        # Aggregation
        # -----------------------------
        pages = result["pages"]

        doc_count += 1
        total_pages += pages
        total_time += result["time_sec"]

        cer_sum += ocr_metrics["CER"] * pages
        wer_sum += ocr_metrics["WER"] * pages
        char_acc_sum += ocr_metrics["Char_Accuracy"] * pages
        fin_sum += fin_metrics["financial_overall_score"]

        f1_sum += f1
        extraction_sum += extraction_acc

        per_doc_results.append({
            "pdf": pdf.name,
            "CER": ocr_metrics["CER"],
            "WER": ocr_metrics["WER"],
            "Char_Accuracy": ocr_metrics["Char_Accuracy"],
            "Financial_Score": fin_metrics["financial_overall_score"],
            "F1": f1,
            "Extraction_Accuracy": extraction_acc
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
        "average_f1_score": round(f1_sum / doc_count, 4),
        "average_extraction_accuracy": round(extraction_sum / doc_count, 4),
        "average_time_per_page_sec": round(total_time / total_pages, 4),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Financial OCR Benchmark Runner")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    run_benchmark(Path(args.dataset))
