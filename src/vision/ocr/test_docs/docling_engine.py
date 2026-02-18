 # ============================================================
 #docling_engine.py

import time
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from PyPDF2 import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
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


def has_embedded_text(pdf_path: str) -> bool:
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages[:3]:
            if page.extract_text():
                return True
        return False
    except Exception:
        return False


# -----------------------------
# PDF Split Helper
# -----------------------------
def create_temp_pdf(original_path: Path, start_page: int, end_page: int) -> Path:
    reader = PdfReader(str(original_path))
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    temp_path = original_path.parent / f"__temp_{original_path.name}"

    with open(temp_path, "wb") as f:
        writer.write(f)

    return temp_path


# -----------------------------
# Docling OCR Engine
# -----------------------------
class OCREngine:

    def __init__(self):
        logger.info("Docling OCR Engine initialized")

    def _clean_text(self, text: str) -> str:
        import re
        text = text.encode("ascii", "ignore").decode()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _create_converter(self, force_ocr: bool = False):

        pipeline_options = PdfPipelineOptions()

        pipeline_options.do_ocr = force_ocr
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        pipeline_options.enable_remote_services = False

        return DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

    # -----------------------------
    # Main OCR method
    # -----------------------------
    def process_pdf(
        self,
        pdf_path: str,
        progress_cb: Optional[Callable[[str], None]] = None,
        start_page: Optional[int] = None,
        end_page: Optional[int] = None
    ) -> Dict[str, Any]:

        pdf_path = Path(pdf_path).expanduser().resolve()

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        if not is_valid_pdf(str(pdf_path)):
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

            # -----------------------------
            # Split PDF if needed
            # -----------------------------
            temp_pdf = pdf_path

            if start_page and end_page:
                if start_page < 1 or end_page > total_pages:
                    raise ValueError("Invalid page range")

                notify(f"Processing pages {start_page}-{end_page}")
                temp_pdf = create_temp_pdf(pdf_path, start_page, end_page)

            notify("OCR started — processing pages")

            # -----------------------------
            # Progress simulation
            # -----------------------------
            progress = {"page": 0}
            stop_flag = {"done": False}

            pages_to_process = (
                end_page - start_page + 1
                if start_page and end_page
                else total_pages
            )

            def progress_simulator():
                while not stop_flag["done"] and progress["page"] < pages_to_process:
                    time.sleep(1.5)
                    progress["page"] += 1
                    notify(f"Processing page {progress['page']} of {pages_to_process}")

            t = threading.Thread(target=progress_simulator, daemon=True)
            t.start()

            # -----------------------------
            # Run Docling
            # -----------------------------
            start_time = time.time()

            embedded = has_embedded_text(str(temp_pdf))
            notify(f"Embedded text detected: {embedded}")

            converter = self._create_converter(force_ocr=not embedded)
            result = converter.convert(str(temp_pdf))

            elapsed = round(time.time() - start_time, 2)

            stop_flag["done"] = True
            t.join()

            # Clean temp file
            if temp_pdf != pdf_path and temp_pdf.exists():
                temp_pdf.unlink()

            notify("OCR completed successfully")

            doc = result.document

            # =============================
            # TEXT (KEEP ORIGINAL)
            # =============================
            raw_text = doc.export_to_text()

            # minimal cleaning (SAFE)
            import re
            cleaned_text = re.sub(r"\s+", " ", raw_text).strip()

            # =============================
            # TABLE EXTRACTION (IMPROVED)
            # =============================
            tables_output = []

            for i, table in enumerate(doc.tables):

                table_dict = {
                    "table_id": i,
                    "rows": []
                }

                try:
                    for row in table.cells:
                        row_data = []

                        for cell in row:
                            cell_text = cell.text.strip() if cell.text else ""
                            row_data.append(cell_text)

                        table_dict["rows"].append(row_data)

                except Exception:
                    # fallback (some tables may be irregular)
                    continue

                tables_output.append(table_dict)

            # =============================
            # RETURN FINAL OUTPUT
            # =============================
            return {
                "success": True,
                "text": raw_text,                     # 🔥 keep original
                "cleaned_text": cleaned_text,         # 🔥 optional
                "tables": tables_output,              # 🔥 IMPORTANT
                "markdown": doc.export_to_markdown(), # 🔥 structure
                "pages": pages_to_process,
                "time_sec": elapsed
            }
        
        except Exception as e:
            logger.error(f"OCR failed for {pdf_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


