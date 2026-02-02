import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, LayoutModelConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCREngine:
    """
    Wrapper for Docling to provide high-fidelity OCR and document structure extraction.
    """
    
    def __init__(self, use_ocr: bool = True, thrust: bool = True):
        """
        Initialize the OCR Engine.
        
        Args:
            use_ocr: Whether to perform OCR on images/scanned pages.
            thrust: Whether to use accelerated processing (if available).
        """
        logger.info("Initializing OCREngine with Docling...")
        
        # Configure pipeline options
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = use_ocr
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        
        # SECURITY: Ensure all processing is LOCAL. No data is sent to the cloud.
        # Models are downloaded once to the local cache, but inference happens here.
        pipeline_options.enable_remote_services = False
        
        # Revert to standard Layout Model as experimental one is gated/unavailable without auth
        # pipeline_options.layout_options.model_spec = LayoutModelConfig(
        #     name="docling_experimental_table_crops_layout",
        #     repo_id="docling-project/docling-experimental-table-crops-layout",
        #     revision="main",
        #     model_path=""
        # )
        
        # Initialize converter with specific PDF options
        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        logger.info("OCREngine initialized.")

    def process_pdf(self, pdf_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert a PDF to structured Markdown and JSON.
        
        Args:
            pdf_path: Path to the input PDF file.
            output_dir: Directory to save the outputs.
            
        Returns:
            Dictionary containing paths to generated files or result data.
        """
        pdf_path_obj = Path(pdf_path)
        if not pdf_path_obj.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            result = self.converter.convert(pdf_path)
            
            # Export to Markdown and Dict (JSON-serializable)
            markdown_content = result.document.export_to_markdown()
            json_dict = result.document.export_to_dict()
            
            output_paths = {}
            
            if output_dir:
                out_path = Path(output_dir)
                out_path.mkdir(parents=True, exist_ok=True)
                
                # Save Markdown
                md_file = out_path / f"{pdf_path_obj.stem}.md"
                md_file.write_text(markdown_content)
                output_paths["markdown"] = str(md_file)
                
                # Save JSON
                json_file = out_path / f"{pdf_path_obj.stem}.json"
                with open(json_file, "w") as f:
                    json.dump(json_dict, f, indent=2)
                output_paths["json"] = str(json_file)
                
                logger.info(f"Output saved to: {output_dir}")
            
            return {
                "success": True,
                "markdown": markdown_content,
                "data": json_dict,
                "output_paths": output_paths
            }
            
        except Exception as e:
            logger.error(f"Error during PDF processing: {e}")
            return {
                "success": False,
                "error": str(e)
            }

if __name__ == "__main__":
    # Quick test if run directly
    import argparse
    parser = argparse.ArgumentParser(description="Run OCR Engine on a PDF.")
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("--output_dir", help="Directory to save outputs.", default="data/processed")
    
    args = parser.parse_args()
    
    engine = OCREngine()
    result = engine.process_pdf(args.pdf_path, args.output_dir)
    
    if result["success"]:
        print(f"Successfully processed {args.pdf_path}")
        for k, v in result["output_paths"].items():
            print(f"- {k.capitalize()}: {v}")
    else:
        print(f"Failed: {result['error']}")
