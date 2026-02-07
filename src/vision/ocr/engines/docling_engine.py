import time
from pathlib import Path
from typing import Dict, Any
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from PyPDF2 import PdfReader

class OCREngine:

    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.enable_remote_services = False

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

    def process_pdf(
                        self,
                        pdf_path: str,
                        output_dir: str | None = None,
                        progress_cb=None
                    ) -> Dict[str, Any]:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        start = time.time()
        result = self.converter.convert(pdf_path)
        elapsed = round(time.time() - start, 2)

        markdown = result.document.export_to_markdown()
        plain_text = result.document.export_to_text()

        return {
            "text": plain_text,
            
            "pages": total_pages,
            "time_sec": elapsed
        }
