import time
import logging
from pathlib import Path
from typing import Optional, Callable, Dict, Any

import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

from engines.base import BaseOCREngine
import os
import shutil


# -----------------------------
# Tesseract binary path (Windows)
# -----------------------------

def resolve_tesseract_path() -> str:
    """
    Resolve Tesseract executable path in a portable way.
    Priority:
    1. Environment variable TESSERACT_PATH
    2. System PATH lookup
    """
    env_path = os.getenv("TESSERACT_PATH")
    if env_path and os.path.exists(env_path):
        return env_path

    system_path = shutil.which("tesseract")
    if system_path:
        return system_path

    raise RuntimeError(
        "Tesseract OCR not found. Please install Tesseract and add it to PATH "
        "or set the TESSERACT_PATH environment variable."
    )


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


# -----------------------------s
# Tesseract OCR Engine
# -----------------------------
class TesseractEngine(BaseOCREngine):

    

    def __init__(self, dpi: int = 300, **kwargs):
        super().__init__(**kwargs)
        self.dpi = dpi

        pytesseract.pytesseract.tesseract_cmd = resolve_tesseract_path()

    def process_pdf(
        self,
        pdf_path: str,
        output_dir: Optional[str] = None,
        progress_cb: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:

        pdf_path = Path(pdf_path).expanduser().resolve()


        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        if not is_valid_pdf(str(pdf_path)):
            logger.error(f"Invalid or corrupted PDF: {pdf_path}")
            return {
                "success": False,
                "error": "Invalid or corrupted PDF",
                "pdf": str(pdf_path)
            }

        try:
            start = time.time()

            images = convert_from_path(
                str(pdf_path),
                dpi=self.dpi
            )

            texts = []
            total_pages = len(images)

            logger.info(f"Starting Tesseract OCR ({total_pages} pages)")

            for i, img in enumerate(images, start=1):
                msg = f"Tesseract OCR: processing page {i}/{total_pages}"
                if progress_cb:
                    progress_cb(msg)
                logger.info(msg)

                texts.append(
                    pytesseract.image_to_string(
                        img,
                        lang="eng",
                        config="--oem 3 --psm 6"
                    )
                )

            elapsed = round(time.time() - start, 2)
            full_text = "\n\n".join(texts)

            logger.info("Tesseract OCR completed successfully")

            return {
                "success": True,
                "text": full_text,
                "markdown": full_text,
                "pages": total_pages,
                "time_sec": elapsed
            }

        except Exception as e:
            logger.exception("Tesseract OCR failed")
            return {
                "success": False,
                "error": str(e),
                "pdf": str(pdf_path)
            }
