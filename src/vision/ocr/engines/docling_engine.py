import time
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from PyPDF2 import PdfReader
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions


# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------
# PDF validation
# -----------------------------
def is_valid_pdf(pdf_path: str) -> bool:
    try:
        PdfReader(pdf_path)
        return True
    except Exception:
        return False


# -----------------------------
# Docling OCR Engine
# -----------------------------
class OCREngine:

    def __init__(self, **kwargs):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        pipeline_options.enable_remote_services = False

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

        logger.info("Docling OCR Engine initialized")

    # -----------------------------
    # Main OCR method
    # -----------------------------
    def process_pdf(
        self,
        pdf_path: str,
        output_dir: Optional[str] = None,
        progress_cb: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        if not is_valid_pdf(str(pdf_path)):
            logger.error(f"Invalid or corrupted PDF: {pdf_path}")
            return {
                "success": False,
                "error": "Invalid or corrupted PDF",
                "pdf": str(pdf_path)
            }

        def notify(msg: str):
            if progress_cb:
                progress_cb(msg)
            logger.info(msg)

        try:
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)

            notify(f"PDF loaded successfully ({total_pages} pages detected)")
            notify("OCR started — processing pages")

            # ---- Progress simulation ----
            progress = {"page": 0}
            stop_flag = {"done": False}

            def progress_simulator():
                while not stop_flag["done"] and progress["page"] < total_pages:
                    time.sleep(1.5)
                    progress["page"] += 1
                    notify(f"Processing page {progress['page']} of {total_pages}")

            t = threading.Thread(target=progress_simulator, daemon=True)
            t.start()

            start = time.time()
            result = self.converter.convert(str(pdf_path))
            elapsed = round(time.time() - start, 2)

            stop_flag["done"] = True
            t.join()

            notify("OCR completed successfully")

            markdown = result.document.export_to_markdown()
            plain_text = result.document.export_to_text()

            return {
                "success": True,
                "text": plain_text,
                "markdown": markdown,
                "pages": total_pages,
                "time_sec": elapsed
            }

        except Exception as e:
            logger.exception("OCR processing failed")
            return {
                "success": False,
                "error": str(e),
                "pdf": str(pdf_path)
            }
