import argparse
import json
import sys
from pathlib import Path

from engines.docling_engine import OCREngine
from engines.tesseract_engine import TesseractEngine
from engines.trocr_engine import TrOCREngine

from metrics.accuracy import accuracy_report
from metrics.accuracy_financial import financial_accuracy_report
from metrics.compliance_rules import validate_compliance


# -----------------------------
# Engine registry
# -----------------------------
ENGINES = {
    "docling": OCREngine,
    "tesseract": TesseractEngine,
    "trocr": TrOCREngine,
}


# -----------------------------
# Helpers
# -----------------------------
def extract_gt_text(gt_json: dict) -> str:
    """
    Fully recursive GT extractor.

    - Walks entire JSON structure
    - Collects all string values that look like real OCR/text
    - Skips metadata keys
    - Works for ANY dataset format
    - Automatically future-proof
    """

    collected_text = []
    seen = set()

    # Keys that usually contain non-content metadata
    SKIP_KEYS = {
        "bbox", "box", "id", "id_box", "id_box_line",
        "page_no", "page", "page_start", "page_end",
        "original_width", "original_height",
        "coco_width", "coco_height",
        "metadata", "font", "flags",
        "span_num", "line_num", "block_num"
    }

    def recurse(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in SKIP_KEYS:
                    continue
                recurse(v)

        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

        elif isinstance(obj, str):
            text = obj.strip()
            if text and text not in seen:
                seen.add(text)
                collected_text.append(text)

        # ignore numbers / None / booleans

    recurse(gt_json)

    return "\n".join(collected_text)



def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def progress_cb(msg: str):
    print(f"[STATUS] {msg}")


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="OCR CLI (Integrated Evaluation Mode)"
    )

    parser.add_argument("pdf", help="Path to input PDF")

    parser.add_argument(
        "--engine",
        default="docling",
        choices=ENGINES.keys(),
        help="OCR engine",
    )

    parser.add_argument("--ground_truth", help="Ground truth JSON file")

    parser.add_argument(
        "--output-format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format",
    )

    parser.add_argument(
        "--strategy",
        choices=["fast", "accurate"],
        default="accurate",
        help="Speed vs accuracy",
    )

    parser.add_argument("--output", help="Optional output path")

    parser.add_argument("--start-page", type=int, default=None)
    parser.add_argument("--end-page", type=int, default=None)

    args = parser.parse_args()

    # -----------------------------
    # Engine config
    # -----------------------------
    engine_kwargs = {}
    if args.engine in {"tesseract", "trocr"}:
        engine_kwargs["dpi"] = 150 if args.strategy == "fast" else 300

    try:
        engine = ENGINES[args.engine](**engine_kwargs)

        result = engine.process_pdf(
            args.pdf,
            progress_cb=progress_cb,
            start_page=args.start_page,
            end_page=args.end_page,
        )

    except Exception as e:
        print("\n❌ OCR failed to start")
        print(f"Error: {e}")
        sys.exit(1)

    if not result.get("success", True):
        print("\n❌ OCR failed gracefully")
        print(f"PDF   : {result.get('pdf')}")
        print(f"Error : {result.get('error')}")
        sys.exit(1)

    # -----------------------------
    # Emit OCR Output
    # -----------------------------
    if args.output_format == "text":
        output_data = result["text"]
    elif args.output_format == "markdown":
        output_data = result.get("markdown", result["text"])
    else:
        output_data = result

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(
            json.dumps(output_data, indent=2)
            if isinstance(output_data, dict)
            else output_data,
            encoding="utf-8",
        )
    else:
        print("\n=== OCR OUTPUT ===")
        print(output_data if isinstance(output_data, str)
              else json.dumps(output_data, indent=2))

    # -----------------------------
    # Evaluation Mode
    # -----------------------------
    if not args.ground_truth:
        return

    with open(args.ground_truth, encoding="utf-8") as f:
        gt_json = json.load(f)

    benchmark_report = {
        "engine": args.engine,
        "pages_processed": result["pages"],
        "time_sec": result["time_sec"],
    }

    # -----------------------------
    # 1️⃣ TECHNICAL OCR ACCURACY
    # -----------------------------
    gt_text = extract_gt_text(gt_json)

    if gt_text.strip():
        print("\n==============================")
        print("📊 TECHNICAL OCR ACCURACY")
        print("==============================")

        technical_metrics = accuracy_report(
            normalize(gt_text),
            normalize(result["text"])
        )

        for k, v in technical_metrics.items():
            print(f"{k}: {v}")

        benchmark_report["technical_accuracy"] = technical_metrics
    else:
        print("\n📊 Technical accuracy skipped (structured GT detected)")
        benchmark_report["technical_accuracy"] = "skipped"

    # -----------------------------
    # 2️⃣ FINANCIAL ACCURACY
    # -----------------------------
    if "tables" in gt_json:
        print("\n==============================")
        print("📈 FINANCIAL ACCURACY")
        print("==============================")

        financial_metrics = financial_accuracy_report(
            gt_json,
            result["text"]
        )

        for k, v in financial_metrics.items():
            print(f"{k}: {v}")

        benchmark_report["financial_accuracy"] = financial_metrics

    # -----------------------------
    # 3️⃣ COMPLIANCE VALIDATION
    # -----------------------------
    if "compliance_cases" in gt_json:
        print("\n==============================")
        print("⚖ COMPLIANCE VALIDATION")
        print("==============================")

        compliance_results = validate_compliance(
            gt_json,
            result["text"]
        )

        for rule in compliance_results:
            print(f"{rule['rule']}: {rule['status']}")

        benchmark_report["compliance"] = compliance_results

    # -----------------------------
    # Save Benchmark Report
    # -----------------------------
    report_path = Path("benchmark_report.json")
    report_path.write_text(
        json.dumps(benchmark_report, indent=2),
        encoding="utf-8"
    )

    print("\n📁 benchmark_report.json saved")


if __name__ == "__main__":
    main()
