import argparse
import json
import sys
import time
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
    "trocr": TrOCREngine
}

# -----------------------------
# Helpers
# -----------------------------
def extract_gt_text_from_pubmed_ocr(gt_json_path: str) -> str:
    """
    Extract line-level ground truth text from PubMed-OCR JSON.
    """
    with open(gt_json_path, encoding="utf-8") as f:
        gt = json.load(f)

    try:
        lines = gt["ocr"]["text"]["lines"]
    except KeyError:
        raise ValueError("Invalid PubMed-OCR GT format")

    return "\n".join(line["text"] for line in lines)


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
        description="OCR Benchmark CLI (T1.1 – Vision Layer)"
    )

    parser.add_argument(
        "pdf",
        help="Path to input PDF file"
    )

    parser.add_argument(
        "--engine",
        default="docling",
        choices=ENGINES.keys(),
        help="OCR engine to use"
    )

    parser.add_argument(
        "--ground_truth",
        help="Ground truth JSON file (PubMed-OCR format)"
    )

    parser.add_argument(
        "--output-format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format to emit"
    )

    parser.add_argument(
        "--strategy",
        choices=["fast", "accurate"],
        default="accurate",
        help="Processing strategy (speed vs accuracy)"
    )

    parser.add_argument(
        "--output",
        help="Optional output file path"
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
        start = time.time()

        result = engine.process_pdf(
            args.pdf,
            progress_cb=progress_cb
        )

        elapsed = time.time() - start

    except Exception as e:
        print("\n❌ OCR failed gracefully")
        print(f"Error: {e}")
        sys.exit(1)

    # -----------------------------
    # Emit output
    # -----------------------------
    output_data = None

    if args.output_format == "text":
        output_data = result["text"]

    elif args.output_format == "markdown":
        output_data = result.get("markdown", result["text"])

    elif args.output_format == "json":
        output_data = result

    if args.output:
        Path(args.output).write_text(
            json.dumps(output_data, indent=2)
            if isinstance(output_data, dict)
            else output_data,
            encoding="utf-8"
        )
    else:
        print("\n=== OCR OUTPUT ===")
        print(output_data if isinstance(output_data, str) else json.dumps(output_data, indent=2))

    # -----------------------------
    # Accuracy (optional)
    # -----------------------------
    if args.ground_truth:
        gt_text = normalize(
            extract_gt_text_from_pubmed_ocr(args.ground_truth)
        )
        pred_text = normalize(result["text"])

        metrics = accuracy_report(gt_text, pred_text)

        print("\n=== OCR BENCHMARK ===")
        print(f"Engine     : {args.engine}")
        print(f"Pages      : {result['pages']}")
        print(f"Time (sec) : {round(elapsed, 2)}")

        print("\n=== ACCURACY (vs PubMed-OCR GT) ===")
        for k, v in metrics.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
