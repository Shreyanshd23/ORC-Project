import argparse
import json
import sys
from pathlib import Path

from engines.docling_engine import OCREngine
from engines.tesseract_engine import TesseractEngine
from engines.trocr_engine import TrOCREngine
from metrics.accuracy import accuracy_report


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
def extract_gt_text(gt_json_path: str) -> str:
    """
    Extract ground-truth text from multiple GT JSON formats.
    Supports:
    - PubMed-OCR
    - Layout annotation (form-based, DocLayNet/PubLayNet style)
    - Line / paragraph OCR
    - Plain text GT
    """
    with open(gt_json_path, encoding="utf-8") as f:
        gt = json.load(f)

    # PubMed-OCR format
    if "ocr" in gt and "text" in gt["ocr"] and "lines" in gt["ocr"]["text"]:
        return "\n".join(line["text"] for line in gt["ocr"]["text"]["lines"])

    # Layout-annotation format (your check_ocr dataset)
    if "form" in gt and isinstance(gt["form"], list):
        texts = [
            block["text"]
            for block in gt["form"]
            if isinstance(block, dict)
            and "text" in block
            and block["text"].strip()
        ]
        return "\n".join(texts)

    # Line-based OCR
    if "lines" in gt and isinstance(gt["lines"], list):
        return "\n".join(line.get("text", "") for line in gt["lines"])

    # Paragraph-based OCR
    if "paragraphs" in gt and isinstance(gt["paragraphs"], list):
        return "\n".join(p.get("text", "") for p in gt["paragraphs"])

    # Plain text GT
    if "text" in gt and isinstance(gt["text"], str):
        return gt["text"]

    raise ValueError("Unsupported ground-truth JSON format")



def normalize(text: str) -> str:
    """
    Light normalization for fair CER/WER comparison.
    """
    return " ".join(text.lower().split())


def progress_cb(msg: str):
    """
    CLI-friendly progress callback.
    """
    print(f"[STATUS] {msg}")


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="OCR CLI (T1.1 – Vision Layer)"
    )

    parser.add_argument("pdf", help="Path to input PDF file")

    parser.add_argument(
        "--engine",
        default="docling",
        choices=ENGINES.keys(),
        help="OCR engine to use",
    )

    parser.add_argument(
    "--ground_truth",
    help="Ground truth JSON file (PubMed-OCR or layout-annotation format)",
    )


    parser.add_argument(
        "--output-format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format to emit",
    )

    parser.add_argument(
        "--strategy",
        choices=["fast", "accurate"],
        default="accurate",
        help="Processing strategy (speed vs accuracy)",
    )

    parser.add_argument(
        "--output",
        help="Optional output file path",
    )

    args = parser.parse_args()

    # -----------------------------
    # Strategy → engine config
    # -----------------------------
    engine_kwargs = {}

    if args.engine in {"tesseract", "trocr"}:
        engine_kwargs["dpi"] = 150 if args.strategy == "fast" else 300

    # -----------------------------
    # Run OCR
    # -----------------------------
    try:
        engine = ENGINES[args.engine](**engine_kwargs)

        result = engine.process_pdf(
            args.pdf,
            progress_cb=progress_cb,
        )

    except Exception as e:
        print("\n❌ OCR failed to start")
        print(f"Error: {e}")
        sys.exit(1)

    # -----------------------------
    # Handle engine-level failure
    # -----------------------------
    if not result.get("success", True):
        print("\n❌ OCR failed gracefully")
        print(f"PDF   : {result.get('pdf')}")
        print(f"Error : {result.get('error')}")
        sys.exit(1)

    # -----------------------------
    # Emit output
    # -----------------------------
    if args.output_format == "text":
        output_data = result["text"]

    elif args.output_format == "markdown":
        output_data = result.get("markdown", result["text"])

    else:  # json
        output_data = result

    if args.output:
        Path(args.output).write_text(
            json.dumps(output_data, indent=2)
            if isinstance(output_data, dict)
            else output_data,
            encoding="utf-8",
        )
    else:
        print("\n=== OCR OUTPUT ===")
        print(
            output_data
            if isinstance(output_data, str)
            else json.dumps(output_data, indent=2)
        )

    # -----------------------------
    # Accuracy (optional)
    # -----------------------------
    if args.ground_truth:
        gt_text = normalize(
            extract_gt_text(args.ground_truth)
        )
        pred_text = normalize(result["text"])

        metrics = accuracy_report(gt_text, pred_text)

        print("\n=== OCR BENCHMARK ===")
        print(f"Engine     : {args.engine}")
        print(f"Pages      : {result['pages']}")
        print(f"Time (sec) : {result['time_sec']}")

        print("\n=== ACCURACY (vs PubMed-OCR GT) ===")
        for k, v in metrics.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
