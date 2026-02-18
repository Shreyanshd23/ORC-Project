
import time
import logging
from pathlib import Path
from typing import Dict, Any

import numpy as np
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

from PyPDF2 import PdfReader
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions


# ---- SET YOUR TESSERACT PATH HERE ----
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


logger = logging.getLogger(__name__)


class HybridOCREngine:
    """
    TRUE Hybrid OCR Engine

    Uses:
        Docling → layout + tables
        Tesseract → paragraph text

    Routing logic:
        table page → Docling OCR
        text page → Tesseract OCR
    """

    def __init__(self):
        logger.info("Initializing Hybrid OCR Engine")

        opts = PdfPipelineOptions()
        opts.do_ocr = True
        opts.do_table_structure = True
        opts.table_structure_options.do_cell_matching = True
        opts.enable_remote_services = False

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=opts)
            }
        )

    # --------------------------------------------------
    def _page_has_table(self, page):
        for block in getattr(page, "blocks", []):
            if getattr(block, "label", "") == "table":
                return True
        return False

    # --------------------------------------------------
    def _valid_pdf(self, path):
        try:
            PdfReader(path)
            return True
        except Exception:
            return False

    # --------------------------------------------------
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            return {"success": False, "error": "File not found"}

        if not self._valid_pdf(str(pdf_path)):
            return {"success": False, "error": "Invalid PDF"}

        start = time.time()

        reader = PdfReader(str(pdf_path))
        page_count = len(reader.pages)

        # ---------- Docling Layout Pass ----------
        result = self.converter.convert(str(pdf_path))
        doc = result.document

        # ---------- Renderer ----------
        pdf = fitz.open(str(pdf_path))

        pages_text = []

        for i, page in enumerate(doc.pages.values()):

            # -------- TABLE PAGE → Docling OCR --------
            if self._page_has_table(page):
                pages_text.append(page.export_to_text())
                continue

            # -------- TEXT PAGE → Tesseract OCR --------
            pix = pdf[i].get_pixmap(dpi=300, alpha=False)

            img = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(pix.h, pix.w, 3)

            pil_img = Image.fromarray(img)

            text = pytesseract.image_to_string(pil_img, lang="eng")

            pages_text.append(text.strip())

        elapsed = round(time.time() - start, 2)

        return {
            "success": True,
            "text": "\n".join(pages_text),
            "markdown": doc.export_to_markdown(),
            "data": doc.export_to_dict(),
            "pages": page_count,
            "time_sec": elapsed
        }

