# Financial OCR Benchmark Runner

A comprehensive benchmarking framework for evaluating OCR engines on financial documents. This runner processes PDF documents, extracts text using an OCR engine, and computes multiple accuracy metrics including technical OCR quality, financial content accuracy, information extraction F1 scores, and compliance validation.

## Overview

The benchmark runner automates the evaluation of OCR performance on financial documents by:
- Processing PDF files with page range limits
- Loading ground truth JSON annotations
- Computing technical OCR metrics (CER, WER, Character Accuracy)
- Evaluating financial content accuracy (numeric, line items, sections, disclosures)
- Measuring information extraction quality (F1, Precision, Recall)
- Validating compliance with financial reporting requirements
- Generating comprehensive per-document and aggregated reports

## Dependencies

### External Modules
- `argparse`: Command-line argument parsing
- `json`: JSON file handling
- `pathlib`: Path manipulation
- `structure_builder`: Builds structured JSON from OCR output
- `engines.docling_engine`: OCR engine interface
- `metrics.accuracy`: Technical OCR metrics (CER, WER)
- `metrics.accuracy_financial_new`: Financial content accuracy metrics
- `metrics.compliance_rules`: Compliance validation rules

## Core Functions

### `normalize(text: str) -> str`
Normalizes text by converting to lowercase and collapsing whitespace for consistent comparison.

### `extract_gt_text(gt_json) -> str`
Recursively extracts all text strings from ground truth JSON structure.

**Parameters:**
- `gt_json`: Nested JSON structure containing ground truth annotations

**Returns:**
- Concatenated string of all text values found in the JSON

### `compute_f1(gt_json, pred_json) -> Tuple[float, float, float]`
Computes F1 score, precision, and recall for key information extraction.

**Method:**
- Recursively extracts key-value pairs from both JSON structures
- Converts to lowercase for case-insensitive matching
- Treats each (key, value) pair as a unique entity
- Computes true positives as intersection of entity sets

**Returns:**
- `(f1_score, precision, recall)` rounded to 4 decimal places

### `compute_extraction_accuracy(gt_json, pred_text) -> float`
Simple token-based accuracy measure comparing ground truth JSON string with predicted text.

**Method:**
- Converts ground truth to lowercase JSON string
- Splits into tokens
- Counts tokens present in predicted text

## Main Function

### `run_benchmark(dataset_dir: Path)`
Orchestrates the complete benchmark execution for all PDFs in a dataset directory.

**Parameters:**
- `dataset_dir`: Path to directory containing:
  - PDF files (`*.pdf`)
  - Ground truth JSON files (`*_gt.json`)
  - Optional `page_limits.json` for page range specifications

### Page Limits Configuration

Optional `page_limits.json` format:
```json
{
    "document1.pdf": {
        "start_page": 1,
        "end_page": 10
    },
    "document2.pdf": {
        "start_page": 3,
        "end_page": 15
    }
}
```
# Benchmark Process Flow

For each PDF document:

    Load Configuration

        Check for page limits

        Verify ground truth file exists

    Process PDF

        Initialize OCR engine

        Process specified page range

        Handle OCR failures gracefully

    Load Ground Truth

        Parse corresponding *_gt.json file

        Extract all text for comparison

    Compute Metrics

    Save Output

        Generate structured JSON output (*_output.json)

        Store all metrics for aggregation

    Aggregate Results

        Running sums for weighted averages

        Per-document tracking for detailed reporting
# Benchmark Full Report
Structure:
```python
{
    "per_document_results": [
        {
            "pdf": "document1.pdf",
            "CER": 0.0234,
            "WER": 0.1567,
            "Char_Accuracy": 0.9766,
            "Financial_Score": 0.8456,
            "F1": 0.7234,
            "Extraction_Accuracy": 0.8912
        }
    ],
    "final_summary": {
        "documents_processed": 10,
        "total_pages": 147,
        "average_CER": 0.0215,
        "average_WER": 0.1489,
        "average_character_accuracy": 0.9785,
        "average_financial_score": 0.8321,
        "average_f1_score": 0.7145,
        "average_extraction_accuracy": 0.8867,
        "average_time_per_page_sec": 2.3456
    }
}
```

# Key Features
✅ Comprehensive Metrics

    Technical OCR quality (CER, WER)

    Financial content accuracy

    Information extraction quality (F1)

    Compliance validation

✅ Intelligent Aggregation

    Page-weighted averages for CER/WER

    Document-level averaging for other metrics

    Per-document tracking for detailed analysis

✅ Robust Error Handling

    Skips documents with missing ground truth

    Handles OCR failures gracefully

    Continues processing remaining documents

✅ Flexible Processing

    Configurable page ranges per document

    Automatic output file generation

    Structured JSON output matching ground truth forma