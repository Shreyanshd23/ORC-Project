# Data Structure Overview

data/
├── benchmarks/
│   ├── fintabnet/                     # Financial table benchmark
│   │   ├── raw_parquet/               # Source parquet files (NOT committed)
│   │   ├── pdf/                       # Synthesized single-page PDFs
│   │   └── gt_json/                   # OCR-style ground truth (generated)
│   │
│   ├── doclaynet/                     # Complex document layout benchmark
│   │   ├── raw_json/val/              # Source COCO-style annotations
│   │   ├── images/                    # Page images (dataset-provided)
│   │   ├── pdf/                       # Synthesized single-page PDFs
│   │   └── gt_json/                   # OCR-style ground truth (generated)
│   │
│   ├── icdar2013/                     # Text OCR baseline
│   │   ├── pdf/
│   │   └── gt_json/
│   │
│   └── README.md                      # Dataset preparation & usage


# 📊 Benchmark Datasets

## 1. FinTabNet – Financial Table Documents

Source: HuggingFace (FinTabNet validation split)

Original Format:
- Parquet files containing table annotations and rendered page images

Pipeline Format:
- Page images → single-page PDFs (synthesized)
- Table HTML / restored text → OCR-style ground truth JSON

Purpose:
- Evaluate OCR robustness on financial documents containing dense tables
- Measure text extraction accuracy in table-heavy layouts (CER/WER)
## 2. DocLayNet – Complex Document Layouts

Source: Kaggle (DocLayNet validation split)

Original Format:
- Page images + COCO-style layout annotations

Pipeline Format:
- Page images → single-page PDFs (synthesized)
- Layout text regions → OCR-style ground truth JSON

Purpose:
- Evaluate OCR performance on complex multi-region documents
- Stress-test layout-heavy financial and report-style pages
## 3. ICDAR 2013 – Text OCR Baseline

Source: Synthetic scaffold aligned with ICDAR 2013 format

Format:
- PDF documents
- Line- and word-level OCR ground truth JSON

Purpose:
- Establish a clean baseline for pure text OCR
- Validate metric correctness independent of layout complexity

# 🛠️ Scripts Documentation

# Data Processing Scripts

convert_fintabnet.py

Purpose: Convert FinTabNet parquet files to JSON format
Input: data/benchmarks/fintabnet/raw_parquet/*.parquet
Output: data/benchmarks/fintabnet/gt_json/FinTabNet_OTSL_val.json
Key Features:

    Reads multiple parquet files

    Combines into single JSON

    Handles numpy serialization issues

    Preserves table structure data (otsl, html, cells)

process_doclaynet.py

Purpose: Process DocLayNet JSON files for benchmarking
Input: data/benchmarks/doclaynet/raw_json/val/*.json
Output: data/benchmarks/doclaynet/gt_json/DocLayNet_val.json
Key Features:

    Loads and combines multiple JSON files

    Validates COCO annotation format

    Extracts layout and region data

    Ensures consistent structure

Validation & Verification Scripts
validate_benchmarks.py

Purpose: Validate all benchmark datasets
Checks:

    JSON syntax validity

    Minimum record counts

    Required field presence

    Data structure consistency

    File size expectations

Usage:

python validate_benchmarks.py

create_icdr_sample.py

Purpose:Creates a synthetic placeholder dataset for ICDAR 2013 benchmark when the actual dataset is not immediately available. Establishes the data format and pipeline structure for pure text OCR validation during the T0.3 planning phase

Core Operations

    Generates Synthetic Document Data - Creates realistic text samples mimicking ICDAR 2013 format

    Establishes JSON Structure - Defines exact format expected by evaluation pipeline

    Sets Up Directory Structure - Creates required folder hierarchy automatically

    Provides Validation Samples - Enables immediate pipeline testing

Output Format

[
  {
    "id": "icdar_001",
    "text": "Full document text for OCR testing",
    "lines": [
      {"text": "Line 1 text", "bbox": [x, y, width, height]},
      {"text": "Line 2 text", "bbox": [x, y, width, height]}
    ],
    "words": [
      {"text": "Word1", "bbox": [x, y, width, height]},
      {"text": "Word2", "bbox": [x, y, width, height]}
    ]
  }
]

# 🚀 Quick Start
1. Setup Environment
bash

# Create directory structure
mkdir -p data/benchmarks/{fintabnet,doclaynet,icdar2013}/{raw,gt_json}
mkdir -p data/ground_truth


2. Download Data


 Download FinTabNet
 Download manually from HuggingFace(download the val_*.paquet files) and place them in data/benchmark/fintabnet/gt_json

 Download DocLayNet (from Kaggle)
 Manual download required: val.json → data/benchmarks/doclaynet/raw_json/val/

 Run the python create_icdar_sample.py

3. Process Data


# Convert FinTabNet
python convert_fintabnet.py

# Process DocLayNet
python process_doclaynet.py



4. Validate


# Validate all benchmarks
python validate_benchmarks.py


📈 Evaluation Metrics
FinTabNet Metrics

    Table Detection Accuracy

    Cell Recognition Accuracy

    HTML Structure Fidelity

DocLayNet Metrics

    Layout Parsing Accuracy

    Region Detection F1 Score

    Bounding Box IoU

ICDAR 2013 Metrics

    Character Recognition Rate (CRR)

    Word Accuracy

    Line Detection Accuracy


