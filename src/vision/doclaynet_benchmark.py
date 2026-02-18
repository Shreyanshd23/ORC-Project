import json
import argparse
from pathlib import Path
from typing import Dict


from metrics.accuracy import accuracy_report


# -----------------------------
# Engine Registry
# -----------------------------
ENGINES = {
    "docling": "engines.docling_engine.OCREngine",
    "hybrid": "engines.hybrid_engine.HybridOCREngine",
    "native": "engines.docling_native_engine.DoclingNativeEngine",
}



# -----------------------------
# Extract GT text (DocLayNet format)
# -----------------------------
def extract_doclaynet_text(gt_json: dict) -> str:
    texts = []

    if "form" in gt_json:
        for block in gt_json["form"]:
            if isinstance(block, dict) and "text" in block:
                texts.append(block["text"])

    if "lines" in gt_json:
        for line in gt_json["lines"]:
            texts.append(line.get("text", ""))

    return "\n".join(texts)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


# -----------------------------
# Aggregator
# -----------------------------
class BenchmarkAggregator:

    def __init__(self):
        self.total_pages = 0
        self.total_time = 0
        self.cer_sum = 0
        self.wer_sum = 0
        self.char_acc_sum = 0
        self.doc_count = 0

    def add(self, pages: int, time_sec: float, metrics: Dict):

        self.total_pages += pages
        self.total_time += time_sec
        self.doc_count += 1

        self.cer_sum += metrics["CER"] * pages
        self.wer_sum += metrics["WER"] * pages
        self.char_acc_sum += metrics["Char_Accuracy"] * pages

    def final(self):

        if self.total_pages == 0:
            return {}

        return {
            "documents_processed": self.doc_count,
            "total_pages": self.total_pages,
            "average_CER": round(self.cer_sum / self.total_pages, 4),
            "average_WER": round(self.wer_sum / self.total_pages, 4),
            "average_character_accuracy": round(self.char_acc_sum / self.total_pages, 4),
            "average_time_per_page_sec": round(self.total_time / self.total_pages, 4),
        }


# -----------------------------
# MAIN
# -----------------------------
def run_doclaynet_benchmark(dataset_dir: Path, engine_name: str):

    if engine_name not in ENGINES:
        print(f"❌ Unknown engine: {engine_name}")
        return

    import importlib

    module_path, class_name = ENGINES[engine_name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    engine_class = getattr(module, class_name)

    engine = engine_class()

    aggregator = BenchmarkAggregator()

    pdf_files = list(dataset_dir.glob("*.pdf"))

    if not pdf_files:
        print("❌ No PDFs found in dataset folder")
        return

    for pdf_path in pdf_files:

        gt_path = pdf_path.with_suffix(".json")

        if not gt_path.exists():
            print(f"⚠ Skipping {pdf_path.name} — No GT JSON found")
            continue

        print(f"\n🔍 Processing: {pdf_path.name}")

        result = engine.process_pdf(str(pdf_path))

        if not result["success"]:
            print(f"❌ OCR failed: {pdf_path.name}")
            continue

        with open(gt_path, encoding="utf-8") as f:
            gt_json = json.load(f)

        gt_text = extract_doclaynet_text(gt_json)
        pred_text = result["text"]

        if not gt_text.strip():
            print(f"⚠ No GT text found in {gt_path.name}")
            continue

        metrics = accuracy_report(
            normalize(gt_text),
            normalize(pred_text)
        )

        aggregator.add(
            pages=result["pages"],
            time_sec=result["time_sec"],
            metrics=metrics
        )

        print("CER:", round(metrics["CER"], 4))
        print("WER:", round(metrics["WER"], 4))

    final = aggregator.final()

    print("\n==============================")
    print(f"📊 DOCLAYNET BENCHMARK RESULTS ({engine_name.upper()})")
    print("==============================")

    for k, v in final.items():
        print(f"{k}: {v}")

    output_file = f"doclaynet_benchmark_summary_{engine_name}.json"

    Path(output_file).write_text(
        json.dumps(final, indent=2),
        encoding="utf-8"
    )

    print(f"\n📁 {output_file} saved")


# -----------------------------
# CLI Entry
# -----------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default=r"C:\Users\dewan\AI-FRC\data\benchmark\DocLayNet\test\pdfs",
        help="Path to dataset folder"
    )
    parser.add_argument(
        "--engine",
        default="docling",
        choices=ENGINES.keys(),
        help="OCR engine to use"
    )

    args = parser.parse_args()

    run_doclaynet_benchmark(
        dataset_dir=Path(args.dataset),
        engine_name=args.engine
    )
