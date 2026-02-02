import argparse
import sys
from pathlib import Path
from src.vision.ocr_engine import OCREngine

def main():
    parser = argparse.ArgumentParser(description="AI-FRC Vision Layer: Extract text and tables from Annual Reports.")
    parser.add_argument("--input", "-i", type=str, help="Path to input PDF or directory of PDFs.")
    parser.add_argument("--output", "-o", type=str, default="data/processed", help="Directory to save processed results.")
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR (use only embedded text).")
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = OCREngine(use_ocr=not args.no_ocr)
    
    input_path = Path(args.input) if args.input else Path("data/raw")
    output_dir = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input path {input_path} does not exist.")
        sys.exit(1)
        
    # Find PDF files
    if input_path.is_file():
        pdfs = [input_path]
    else:
        pdfs = list(input_path.glob("*.pdf"))
        
    if not pdfs:
        print(f"No PDF files found in {input_path}")
        return
        
    print(f"Found {len(pdfs)} files to process.")
    
    for pdf in pdfs:
        print(f"--- Processing: {pdf.name} ---")
        result = engine.process_pdf(str(pdf), str(output_dir))
        
        if result["success"]:
            print(f"DONE (Extraction): {result['output_paths'].get('markdown')}")
        else:
            print(f"FAILED: {result.get('error')}")

if __name__ == "__main__":
    main()
