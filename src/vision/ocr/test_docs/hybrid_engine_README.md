# Hybrid OCR Engine

A true hybrid OCR engine that intelligently routes pages to the most appropriate OCR engine based on content type: **Docling for table-heavy pages** and **Tesseract for text-heavy pages**. This approach combines the strengths of both engines for optimal accuracy.

## Overview

The Hybrid OCR Engine implements a smart routing strategy:
- **Table Pages**: Processed with Docling (excellent table structure preservation)
- **Text Pages**: Processed with Tesseract (superior paragraph text recognition)
- **Layout Analysis**: Uses Docling's layout detection to classify pages

This ensures that tables are properly structured while paragraph text benefits from Tesseract's mature OCR engine.

## Dependencies

### External Libraries
- `fitz` (PyMuPDF): PDF rendering and page extraction
- `pytesseract`: Tesseract OCR engine wrapper
- `PIL` (Pillow): Image processing
- `numpy`: Image array manipulation
- `PyPDF2`: PDF validation
- `docling`: Layout analysis and table OCR

### System Requirements
- **Tesseract-OCR** must be installed separately
- Path to Tesseract executable must be configured

## Tesseract Configuration

The engine includes a hardcoded path to Tesseract:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

```
# You must:

    Install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki

    Verify/update the path to match your installation

    Ensure English language pack is installed

# Class: HybridOCREngine
## Initialization
python

engine = HybridOCREngine()

Initialization Process:

    Configures Docling pipeline options:

        do_ocr = True: Enable OCR for scanned content

        do_table_structure = True: Detect and preserve table structure

        do_cell_matching = True: Match cells within tables

        enable_remote_services = False: Offline operation only

Private Methods
_page_has_table(page) -> bool

Determines if a page contains tables based on Docling's layout analysis.

## Parameters:

    page: Docling page object from document.pages

## Returns:

    True if any block in the page has label "table"

    False otherwise

## _valid_pdf(path) -> bool

Validates PDF file integrity using PyPDF2.

### Parameters:

    path: Path to PDF file

### Returns:

    True if PDF can be opened and read

    False if corrupted or invalid

## Main Processing Method
process_pdf(pdf_path: str) -> Dict[str, Any]

Processes a PDF document using hybrid routing strategy.

### Parameters:

    pdf_path: Path to PDF file (string or Path-like)


# Processing Flow
Step 1: PDF Validation
text

Check file exists → Validate PDF integrity → Get page count

Step 2: Docling Layout Analysis
text

Convert PDF with Docling → Extract layout information → Identify table pages

This pass provides:

    Page-level layout blocks with labels

    Table structure detection

    Markdown and dictionary exports

Step 3: Page-by-Page Processing

For each page in the document:
Table Pages (Docling route)

    Uses text already extracted by Docling during layout pass

    Preserves table structure and cell relationships

    Fast (no additional processing)

Text Pages (Tesseract route)

    Render page with PyMuPDF at 300 DPI

    Convert to numpy array

    Transform to PIL Image

    Run Tesseract OCR with English language

    Extract and clean text

Step 4: Result Aggregation

    Combine all page texts with newlines

    Collect timing information

    Return comprehensive results

# Technical Details
Page Rendering (Tesseract Route)
python

pix = pdf[i].get_pixmap(dpi=300, alpha=False)

    300 DPI: High quality for OCR accuracy

    alpha=False: No transparency (simpler processing)

Image Conversion Pipeline
text

fitz Pixmap → numpy array (H×W×3) → PIL Image → Tesseract OCR

Docling Configuration
python

opts = PdfPipelineOptions()
opts.do_ocr = True              # Enable OCR for scanned docs
opts.do_table_structure = True   # Detect tables
opts.table_structure_options.do_cell_matching = True  # Match cells
opts.enable_remote_services = False  # Offline mode

Usage Examples
Basic Usage
python

from engines.hybrid_engine import HybridOCREngine

engine = HybridOCREngine()
result = engine.process_pdf("annual_report_2023.pdf")

if result["success"]:
    print(f"Processed {result['pages']} pages in {result['time_sec']} seconds")
    print(f"Total text length: {len(result['text'])} characters")
    
    # Save outputs
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(result["markdown"])
else:
    print(f"Error: {result['error']}")

Batch Processing Multiple Documents
python

from pathlib import Path
from engines.hybrid_engine import HybridOCREngine

engine = HybridOCREngine()
pdf_dir = Path("./documents")

for pdf_path in pdf_dir.glob("*.pdf"):
    print(f"\nProcessing {pdf_path.name}...")
    
    result = engine.process_pdf(str(pdf_path))
    
    if result["success"]:
        # Save text output
        output_path = pdf_path.with_suffix(".txt")
        output_path.write_text(result["text"], encoding="utf-8")
        print(f"  ✓ Saved to {output_path.name}")
        print(f"  ⏱ Time: {result['time_sec']}s")
    else:
        print(f"  ✗ Failed: {result['error']}")

Integrating with Evaluation Pipeline
python

from engines.hybrid_engine import HybridOCREngine
from metrics.accuracy import accuracy_report
import json

engine = HybridOCREngine()

# Process document
result = engine.process_pdf("financial_statement.pdf")

# Load ground truth
with open("financial_statement_gt.json") as f:
    gt_json = json.load(f)

# Extract ground truth text (using your existing extractor)
gt_text = extract_gt_text(gt_json)

# Evaluate
metrics = accuracy_report(gt_text, result["text"])
print(f"CER: {metrics['CER']}, WER: {metrics['WER']}")

# Performance Characteristics
Speed Factors

    Docling Layout Pass: ~2-5 seconds per page (varies by content)

    Tesseract OCR: ~1-3 seconds per text page at 300 DPI

    Page Rendering: ~0.5 seconds per page with PyMuPDF

# Accuracy Considerations

    Table Pages: Docling excels at preserving tabular structure

    Text Pages: Tesseract generally better for paragraph text

    Mixed Pages: Currently routed based on dominant content type

# Memory Usage

    Full PDF loaded into memory (PyMuPDF)

    Docling maintains document model

    300 DPI images consume significant memory for large pages

Error Handling
File Errors
python

# Missing file
result = engine.process_pdf("nonexistent.pdf")
# Returns: {"success": False, "error": "File not found"}

# Corrupted PDF
result = engine.process_pdf("corrupted.pdf")
# Returns: {"success": False, "error": "Invalid PDF"}

# Processing Errors

If an error occurs during processing:

    Exception is caught and logged

    Returns error dictionary with details

    No partial results returned

# Configuration Options
Tesseract Path

Update this line to match your installation:
python

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# DPI Setting

Change rendering resolution (default: 300):
python

pix = pdf[i].get_pixmap(dpi=300, alpha=False)  # Adjust 300 to desired DPI

# Docling Pipeline Options

Modify in __init__:
python

opts.do_ocr = True  # Set False if all PDFs have embedded text

Advantages Over Single-Engine Solutions
Aspect	Docling Only	Tesseract Only	Hybrid
Table Structure	✅ Excellent	❌ Poor	✅ Excellent
Paragraph Text	⚠️ Good	✅ Excellent	✅ Excellent
Speed	⚠️ Moderate	✅ Fast	⚠️ Moderate
Layout Detection	✅ Built-in	❌ None	✅ Docling
Scanned Docs	✅ Yes	✅ Yes	✅ Yes
Text PDFs	✅ Yes	✅ Yes	✅ Yes
# Limitations

    Page Classification: Uses simple table presence heuristic

    Mixed Content Pages: Pages with both text and tables use Docling only

    Tesseract Path: Hardcoded path requires manual configuration

    No Page Range: Currently processes entire document

    Memory: 300 DPI images for all pages may be memory-intensive

    Speed: Two-pass processing (layout + per-page) is slower than single-pass

# Troubleshooting
Tesseract Not Found
text

pytesseract.pytesseract.TesseractNotFoundError

Solution: Update the Tesseract path in the code to match your installation.
Memory Issues with Large PDFs

Solution: Reduce DPI or implement batch processing:
python

# Lower DPI to 200 for large documents
pix = pdf[i].get_pixmap(dpi=200, alpha=False)

Poor Table Detection

Solution: Adjust Docling's table detection sensitivity by modifying pipeline options.
Future Enhancements

# Potential improvements to consider:

    Configurable page range processing

    Mixed-content page splitting (extract tables + text separately)

    GPU acceleration for Tesseract

    Caching rendered images

    Parallel page processing

    Dynamic DPI based on page complexity

# Notes

    The engine assumes English language for Tesseract (lang="eng")

    Docling's OCR is used for table pages even if they contain text

    Both engines run in CPU mode by default

    Results include both raw text and structured markdown

    No temporary files are created during processing



