import time
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path
from engines.base import BaseOCREngine

class TrOCREngine(BaseOCREngine):

    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained(
            "microsoft/trocr-base-printed"
        )
        self.model = VisionEncoderDecoderModel.from_pretrained(
            "microsoft/trocr-base-printed"
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def process_pdf(self, pdf_path: str):
        start = time.time()
        images = convert_from_path(pdf_path, dpi=300)

        texts = []
        for img in images:
            pixel_values = self.processor(
                images=img,
                return_tensors="pt"
            ).pixel_values.to(self.device)

            ids = self.model.generate(pixel_values)
            text = self.processor.batch_decode(
                ids,
                skip_special_tokens=True
            )[0]
            texts.append(text)

        elapsed = round(time.time() - start, 2)
        full_text = "\n\n".join(texts)

        return {
            "text": full_text,
            "markdown": full_text,
            "pages": len(images),
            "time_sec": elapsed
        }
