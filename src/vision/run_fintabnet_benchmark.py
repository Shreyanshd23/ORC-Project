import json
import argparse
from pathlib import Path

from engines.docling_engine import OCREngine


from metrics.accuracy import accuracy_report
from metrics.accuracy_financial import financial_accuracy_report


# --------------------------------
# Engine Registry
# --------------------------------
ENGINES = {
    "docling": OCREngine,
    
}


# --------------------------------
# Detect GT Type
# --------------------------------
def detect_gt_type(gt_json):

    if isinstance(gt_json, dict) and "html" in gt_json:
        return "html"

    if isinstance(gt_json, dict) and "tables" in gt_json:
        return "structured"

    if isinstance(gt_json, list):
        return "word_level"

    return "unknown"


# --------------------------------
# Extract Word-Level GT
# --------------------------------
def extract_word_level_text(gt_json):

    return " ".join(
        item["text"]
        for item in gt_json
        if isinstance(item, dict) and "text" in item
    )


# --------------------------------
# Aggregator
# --------------------------------
class FinTabNetAggregator:

    def __init__(self):
        self.total_pages = 0
        self.total_time = 0
        self.financial_scores = []
        self.cer_scores = []
        self.wer_scores = []
        self.doc_count = 0

    def add(self, pages, time_sec, fin=None, text=None):

        self.total_pages += pages
        self.total_time += time_sec
        self.doc_count += 1

        if fin is not None:
            self.financial_scores.append(fin)

        if text:
            self.cer_scores.append(text["CER"])
            self.wer_scores.append(text["WER"])

    def final(self):

        avg_fin = sum(self.financial_scores)/len(self.financial_scores) if self.financial_scores else 0
        avg_cer = sum(self.cer_scores)/len(self.cer_scores) if self.cer_scores else 0
        avg_wer = sum(self.wer_scores)/len(self.wer_scores) if self.wer_scores else 0
        avg_time = self.total_time/self.total_pages if self.total_pages else 0

        return {
            "documents_processed": self.doc_count,
            "total_pages": self.total_pages,
            "average_financial_score": round(avg_fin,4),
            "average_CER": round(avg_cer,4),
            "average_WER": round(avg_wer,4),
            "average_time_per_page_sec": round(avg_time,4)
        }


# --------------------------------
# MAIN
# --------------------------------
def run_fintabnet_benchmark(dataset_dir: Path, engine_name: str):

    if engine_name not in ENGINES:
        print("❌ Unknown engine")
        return

    engine = ENGINES[engine_name]()
    agg = FinTabNetAggregator()

    pdfs = list(dataset_dir.glob("*.pdf"))

    if not pdfs:
        print("❌ No PDFs found")
        return

    for pdf in pdfs:

        gt_path = pdf.with_name(pdf.stem + "_words.json")

        if not gt_path.exists():
            print("⚠ Missing GT:", pdf.name)
            continue

        print("\n🔍", pdf.name)

        result = engine.process_pdf(str(pdf))
        if not result["success"]:
            print("❌ OCR failed")
            continue

        with open(gt_path, encoding="utf-8") as f:
            gt_json = json.load(f)

        gt_type = detect_gt_type(gt_json)

        # =====================================================
        # WORD LEVEL DATASET
        # =====================================================
        if gt_type == "word_level":

            gt_text = extract_word_level_text(gt_json)
            pred = result.get("text","")

            text_metrics = accuracy_report(gt_text.lower(), pred.lower())

            fin_metrics = financial_accuracy_report(gt_json, pred)

            agg.add(
                result.get("pages",1),
                result.get("time_sec",0),
                fin=fin_metrics["financial_overall_score"],
                text=text_metrics
            )

            print("Mode:", gt_type)
            print("CER:", round(text_metrics["CER"],4))
            print("WER:", round(text_metrics["WER"],4))
            print("Financial Score:", fin_metrics["financial_overall_score"])

        # =====================================================
        # STRUCTURED / HTML DATASET
        # =====================================================
        else:

            metrics = financial_accuracy_report(
                gt_json,
                result.get("markdown","")
            )

            agg.add(
                result.get("pages",1),
                result.get("time_sec",0),
                fin=metrics["financial_overall_score"]
            )

            print("Mode:", metrics["mode"])
            print("Score:", metrics["financial_overall_score"])

    final = agg.final()

    print("\n==============================")
    print("📊 FINAL RESULTS")
    print("==============================")

    for k,v in final.items():
        print(k,":",v)

    out = f"fintabnet_benchmark_summary_{engine_name}.json"

    Path(out).write_text(json.dumps(final,indent=2))
    print("\nSaved →", out)


# --------------------------------
# CLI
# --------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--engine", default="docling", choices=ENGINES.keys())

    args = parser.parse_args()

    run_fintabnet_benchmark(Path(args.dataset), args.engine)
