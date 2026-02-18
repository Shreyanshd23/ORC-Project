# Hybrid OCR Pipeline with Layout Classification

A comprehensive OCR pipeline that combines layout classification, EasyOCR text extraction, and post-processing for document analysis. This system intelligently identifies text regions, performs OCR selectively, and generates structured outputs including JSON and Markdown formats.

## Overview

This hybrid pipeline processes PDF documents through multiple stages:
1. **Layout Classification**: Identifies text regions vs. tables using image-based heuristics
2. **Selective OCR**: Applies EasyOCR only to classified text regions for efficiency
3. **Text Classification**: Categorizes extracted lines as headings, paragraphs, or numeric content
4. **Multi-format Output**: Generates both JSON-structured data and human-readable Markdown
5. **Evaluation**: Computes CER and WER metrics against ground truth

## Dependencies

### External Libraries
- `numpy`: Image array manipulation
- `easyocr`: OCR engine
- `pdf2image`: PDF to image conversion
- `Poppler`: Required by pdf2image for PDF rendering

### Standard Library
- `re`: Regular expressions
- `argparse`: Command-line argument parsing
- `json`: JSON file handling
- `pathlib`: Path manipulation

## Core Components

### 1. LayoutClassifier Class

A fast heuristic classifier that identifies text regions in document images.

#### `classify_images(images, start_page=1) -> List[Dict]`

Classifies each page image as either "text" or "table" based on visual features.

**Features Analyzed:**
- Horizontal variance: Standard deviation across rows
- Vertical variance: Standard deviation across columns
- Edge density: Average difference between adjacent pixels

**Classification Logic:**
- If horizontal variance < 15 AND edge density > 5 → "table"
- Otherwise → "text"

**Returns:**
```python
[
    {"page": 1, "label": "text"},
    {"page": 2, "label": "table"},
    # ...
```
# Command Line Usage:-
python textonly.py --dataset /path/to/dataset/directory