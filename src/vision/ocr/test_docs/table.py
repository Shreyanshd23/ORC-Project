from engines.docling_engine import OCREngine
from metrics.accuracy_financial_new import financial_accuracy_report
import re

engine = OCREngine()


def run_table_pipeline(pdf_path, gt_json, start_page=None, end_page=None):

    result = engine.process_pdf(
        pdf_path,
        start_page=start_page,
        end_page=end_page
    )

    if not result["success"]:
        raise Exception("Docling OCR failed")

    financial = financial_accuracy_report(
        gt_json,
        result["markdown"]   # 🔥 IMPORTANT
    )

    return {
        "financial": financial,
        "markdown": result["markdown"],
        "text": result["text"]
    }
