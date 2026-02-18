# Complete OCR Pipeline Suite

A comprehensive modular OCR system combining layout classification, text extraction, table processing, and dual-pipeline evaluation for financial document analysis.

## Overview

This suite consists of four integrated modules that work together to provide a complete document processing solution:

1. **Classifier Module** (`classifier.py`): Page-level layout classification using computer vision
2. **Text Module** (`text.py`): EasyOCR-based text extraction and evaluation
3. **Table Module** (`table.py`): Docling-based table extraction with financial metrics
4. **Merge Module** (`merge.py`): Dual-pipeline orchestrator combining all components

---

# Module 1: Layout Classifier

## `classifier.py`

A computer vision-based layout classifier that distinguishes between text and table pages using edge detection and statistical analysis.

### Dependencies
- `pdf2image`: PDF to image conversion
- `numpy`: Numerical operations
- `cv2` (OpenCV): Image processing

### Class: `LayoutClassifier`

#### `classify(pdf_path: str, start_page=None, end_page=None) -> List[Dict]`

Classifies each page in a PDF as either "text" or "table" based on visual features.

**Parameters:**
- `pdf_path`: Path to PDF file
- `start_page`: First page to process (1-indexed, optional)
- `end_page`: Last page to process (optional)

**Returns:**
```python
[
    {"page": 1, "label": "text"},
    {"page": 2, "label": "table"},
    # ...
]
```

# Classification Features
Feature	Description
Line Count	Number of detected lines using Hough Transform
Edge Density	Proportion of edge pixels from Canny detection
Row Variance	Standard deviation of row averages
Column Variance	Standard deviation of column averages
# Classification Logic

A page is classified as "table" if ANY of these conditions are met:

    More than 30 detected lines

    Edge density > 0.15 (15% of pixels are edges)

    Both row variance AND column variance < 20 (uniform regions)

Otherwise, the page is classified as "text".
# Technical Details

Image Processing Pipeline:

    Convert PDF page to image (120 DPI)

    Convert to grayscale using OpenCV

    Apply Canny edge detection (thresholds: 50, 150)

    Detect lines using Probabilistic Hough Transform

    Compute statistical features

    Apply classification rules


# Hough Transform Parameters:

    threshold: 100 (minimum votes for line detection)

    minLineLength: 50 pixels

    maxLineGap: 10 pixels



# poppler Path Configuration

The classifier uses a hardcoded Poppler path for Windows:
python

poppler_path=r"C:\poppler\Library\bin"

Adjust this path based on your system's Poppler installation.
# Module 2: Text OCR Engine
## text.py

A lightweight OCR module using EasyOCR for text extraction with preprocessing and evaluation capabilities.
## Dependencies

    easyocr: OCR engine

    numpy: Image array manipulation

    re: Regular expressions

    metrics.accuracy: CER/WER calculation

## Global Reader Instance
```python

reader = easyocr.Reader(['en'], gpu=False)
```
    English language support

    CPU mode for compatibility

    Loaded once at module import

## Functions
run_easyocr(image) -> str

Extracts text from a single image using EasyOCR.

## Parameters:

    image: PIL Image object

## Returns:

    Concatenated string of all detected text (space-separated)

## Process:

    Convert PIL image to numpy array

    Run EasyOCR text detection

    Extract text from all results (ignoring confidence scores)

    Join with spaces

## preprocess_text(text: str) -> str

# Prepares text for evaluation by normalizing.

## Operations:

    Convert to lowercase

    Collapse multiple whitespaces

    Strip leading/trailing whitespace

evaluate_text(gt_text: str, pred_text: str) -> Dict

Computes OCR accuracy metrics.

## Parameters:

    gt_text: Ground truth text

    pred_text: Predicted/extracted text

## Returns:

    Dictionary from accuracy_report containing CER and WER

## Process:

    Preprocess both texts

    Call accuracy_report from metrics module

# Usage Example
python

from engines.text import run_easyocr, evaluate_text
from pdf2image import convert_from_path

# Extract text
images = convert_from_path("document.pdf", dpi=120)
text = ""
for img in images[:5]:
    text += run_easyocr(img) + "\n"

# Evaluate
gt_text = "Ground truth text here"
metrics = evaluate_text(gt_text, text)
print(f"CER: {metrics['CER']}, WER: {metrics['WER']}")

# Module 3: Table OCR Engine
## table.py

Specialized table extraction module using Docling OCR engine with financial accuracy evaluation.
Dependencies

    engines.docling_engine: Docling OCR wrapper

    metrics.accuracy_financial_new: Financial metrics

    re: Regular expressions

## Global Engine Instance
python

engine = OCREngine()

Single Docling engine instance reused across calls.
Functions
run_table_pipeline(pdf_path, gt_json, start_page=None, end_page=None) -> Dict

Processes a PDF for table extraction and evaluates financial accuracy.

## Parameters:

    pdf_path: Path to PDF file

    gt_json: Ground truth JSON containing expected tables/data

    start_page: First page to process (optional)

    end_page: Last page to process (optional)

## Returns:
python

{
    "financial": {
        "numeric_accuracy": float,
        "row_accuracy": float,
        "header_accuracy": float,
        "column_accuracy": float,
        "financial_overall_score": float
    },
    "markdown": str,  # Document in markdown format
    "text": str       # Raw extracted text
}

## Process:

    Call Docling OCR engine on specified page range

    Check for OCR success

    Run financial accuracy report using markdown output

    Return combined results

## Key Feature: Markdown-based Evaluation

The pipeline uses Docling's markdown export for financial evaluation because:

    Markdown preserves table structure

    Enables accurate row/column matching

    Better for financial metric calculation

## Error Handling

    Raises exception if Docling OCR fails

    Propagates any underlying engine errors

## Usage Example
python

from engines.table import run_table_pipeline
import json

with open("gt.json") as f:
    gt_json = json.load(f)

results = run_table_pipeline(
    "financial_report.pdf",
    gt_json,
    start_page=5,
    end_page=10
)

print(f"Financial Score: {results['financial']['financial_overall_score']}")
print(f"Markdown length: {len(results['markdown'])}")

# Module 4: Dual OCR Pipeline (Merge)
## merge.py

Orchestrates both text and table pipelines, combines results, and computes final weighted scores.
## Dependencies

    argparse: Command-line parsing

    json: JSON handling

    pathlib: Path manipulation

    pdf2image: PDF to image conversion

    engines.text: Text OCR module

    engines.table: Table OCR module

    metrics.compliance_rules: Compliance validation

## Helper Functions
normalize(text: str) -> str

Basic text normalization (lowercase, whitespace collapse).
extract_gt_text(gt_json) -> str

Recursively extracts all text from ground truth JSON.

## Features:

    Traverses dictionaries, lists, and strings

    Collects non-empty strings

    Returns newline-separated text

## Main Function
run_pipeline(dataset_dir: Path)

Processes all PDFs in a directory through both OCR pipelines.

## Input Directory Structure:
text

dataset/
├── document1.pdf
├── document1_gt.json
├── document2.pdf
├── document2_gt.json
├── page_limits.json (optional)

Optional Page Limits Format:
json

{
    "document1.pdf": {"start_page": 1, "end_page": 10},
    "document2.pdf": {"start_page": 3, "end_page": 15}
}

## Pipeline Flow

For each PDF document:
1. Text OCR Pipeline (EasyOCR)
text

PDF → Convert to Images → EasyOCR → Text Output → CER/WER Metrics

Steps:

    Convert PDF pages to images (120 DPI)

    Apply page range limits

    Run EasyOCR on each page

    Accumulate text with >5 chars

    Compute CER, WER, Character Accuracy

2. Table OCR Pipeline (Docling)
text

PDF → Docling OCR → Markdown → Financial Metrics

Steps:

    Process same page range with Docling

    Generate markdown output

    Compute financial accuracy metrics

    Extract numeric, row, header, column scores

3. Compliance Validation

    Check for required financial sections

    Validate against ground truth expectations

    Display PASS/FAIL for each rule

4. Final Score Calculation
text

Final Score = (Char_Accuracy × 0.4) + (Financial_Score × 0.6)

    40% weight on character-level accuracy

    60% weight on financial content accuracy

## Console Output Example
text

====================================
📄 annual_report_2023.pdf
====================================

--- TEXT OCR (EasyOCR) ---
Processing page 1
Processing page 2
Processing page 3
CER: 0.0234
WER: 0.1567
Char Accuracy: 0.9766

--- TABLE OCR (Docling) ---
Numeric Accuracy: 0.95
Row Accuracy: 0.85
Header Accuracy: 1.0
Column Accuracy: 0.9
Financial Score: 0.92

--- COMPLIANCE ---
Balance Sheet Present: PASS
Statement Of Profit And Loss Present: PASS
Cash Flow Present: FAIL
Auditor Present: PASS

--- FINAL ---
Final Score: 0.9428

## Command Line Usage
bash

python -m engines.merge --dataset /path/to/dataset/directory

## Arguments:

    --dataset (required): Path to directory containing PDFs and ground truth JSONs




## Performance Considerations

    Text pipeline processes all pages in range

    No page limits on table pipeline beyond range

    Compliance checks run on full extracted text

# Module Dependencies Graph
## text

                    ┌─────────────────┐
                    │    merge.py     │
                    └────────┬────────┘
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │   text.py   │  │  table.py   │  │compliance   │
    └──────┬──────┘  └──────┬──────┘  │rules (ext)  │
           ▼                 ▼         └─────────────┘
    ┌─────────────┐  ┌─────────────┐
    │  easyocr    │  │  docling    │
    └─────────────┘  │   engine    │
                     └─────────────┘

## Error Handling

    Missing Ground Truth: Skip document with warning

    OCR Failure: Exception raised and stops current document

    Page Limits: Invalid ranges handled by underlying engines

    Empty Text: Handles gracefully with empty string

# Extending the Pipeline
## Adding New OCR Engines

    Create new module (e.g., new_engine.py)

    Implement consistent interface

    Import in merge.py

    Add to pipeline flow

## Adding New Metrics

    Implement metric function

    Import in appropriate module

    Add to results dictionary

    Update final score calculation if needed

## Best Practices

    Page Limits: Use for large documents to focus on relevant sections

    Ground Truth: Ensure comprehensive JSON with all expected text

    Poppler: Verify installation before running

    Memory: Large PDFs may need batch processing

    GPU: Enable GPU for faster processing on large batches

## Limitations

    EasyOCR confidence scores not used (all results included)

    No table structure preservation in text pipeline

    Compliance rules are keyword-based only

    Final score weights are fixed (0.4/0.6)

    Windows-specific Poppler path hardcoded



