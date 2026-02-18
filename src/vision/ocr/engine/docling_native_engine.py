import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from PyPDF2 import PdfReader
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions


# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def is_valid_pdf(path: str) -> bool:
    try:
        PdfReader(path)
        return True
    except Exception:
        return False


def has_embedded_text(path: str) -> bool:
    try:
        reader = PdfReader(path)
        for page in reader.pages[:3]:
            if page.extract_text():
                return True
        return False
    except Exception:
        return False


# --------------------------------------------------
# Engine
# --------------------------------------------------
class DoclingNativeEngine:
    """
    Production-grade Docling engine

    Uses:
    - RapidOCR → text
    - TableFormer → tables
    - Layout model → structure
    """

    def __init__(self):
        logger.info("Initializing Docling Native Engine")

        opts = PdfPipelineOptions()

        # Smart OCR decision handled dynamically later
        opts.do_ocr = True

        # Enable table extraction
        opts.do_table_structure = True
        opts.table_structure_options.do_cell_matching = True

        # Local only (secure)
        opts.enable_remote_services = False

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=opts)
            }
        )

        logger.info("Docling Native Engine ready")

    # --------------------------------------------------
    def _clean(self, text: str) -> str:
        import re
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    # --------------------------------------------------
    def process_pdf(
        self,
        pdf_path: str,
        progress_cb: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:

        pdf_path = Path(pdf_path).resolve()

        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)

        if not is_valid_pdf(str(pdf_path)):
            return {"success": False, "error": "Invalid PDF"}

        def notify(msg):
            logger.info(msg)
            if progress_cb:
                progress_cb(msg)

        try:
            reader = PdfReader(str(pdf_path))
            pages = len(reader.pages)

            notify(f"Loaded PDF ({pages} pages)")

            start = time.time()

            embedded = has_embedded_text(str(pdf_path))
            notify(f"Embedded text detected: {embedded}")

            # If embedded text exists → disable OCR for speed
            if embedded:
                self.converter.format_to_options[
                    InputFormat.PDF
                ].pipeline_options.do_ocr = False
            else:
                self.converter.format_to_options[
                    InputFormat.PDF
                ].pipeline_options.do_ocr = True

            # ---- Run Docling ----
            result = self.converter.convert(str(pdf_path))

            elapsed = round(time.time() - start, 2)

            notify("Extraction finished")

            text = result.document.export_to_text()
            markdown = result.document.export_to_markdown()
            data = result.document.export_to_dict()

            return {
                "success": True,
                "text": self._clean(text),
                "markdown": markdown,
                "data": data,
                "pages": pages,
                "time_sec": elapsed
            }

        except Exception as e:
            logger.exception("Processing failed")
            return {
                "success": False,
                "error": str(e)
            }
