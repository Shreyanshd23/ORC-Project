import time
import pytesseract
from pdf2image import convert_from_path
from engines.base import BaseOCREngine

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class TesseractEngine(BaseOCREngine):

    def __init__(self, dpi: int = 300, **kwargs):
        super().__init__(**kwargs)
        self.dpi = dpi

    def process_pdf(
        self,
        pdf_path: str,
        output_dir: str | None = None,
        progress_cb=None
    ):
        start = time.time()

        images = convert_from_path(pdf_path, dpi=self.dpi)

        texts = []
        total_pages = len(images)

        for i, img in enumerate(images, start=1):
            if progress_cb:
                progress_cb(f"Tesseract OCR: processing page {i}/{total_pages}")

            texts.append(
                pytesseract.image_to_string(
                    img,
                    lang="eng",
                    config="--oem 3 --psm 6"
                )
            )

        elapsed = round(time.time() - start, 2)
        full_text = "\n\n".join(texts)

        return {
            "text": full_text,
            "markdown": full_text,
            "pages": total_pages,
            "time_sec": elapsed
        }
