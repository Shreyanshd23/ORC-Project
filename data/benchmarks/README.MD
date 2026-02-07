# Data Structure Overview

data/
├── benchmarks/                    # Benchmark data
│   ├── fintabnet/                # Financial table 
│   │   ├── raw_parquet/          # Source parquet 
│   │   └── gt_json/              # Ground truth =
│   ├── doclaynet/                # Complex document 
│   │   ├── raw_json/val/         # Source JSON files
│   │   └── gt_json/              # Ground truth 
│   └── icdar2013/                # Text OCR baseline
│   |    └── gt_json/
|    |    |___gt_txt     # Ground truth JSON files
|    |___pubmed_ocr
|    |__README.MD # Fintabnet,doclaynet,icdar extract
|____ground_truth


# 📊  Benchmark Datasets

1. FinTabNet - Financial Table Recognition

    Source: HuggingFace - FinTabNet OTSL conversion

    Format: Parquet → JSON conversion

    Records: 10,505 validation samples

    Purpose: Test table structure recognition in financial documents

2. DocLayNet - Complex Document Layout

    Source: Kaggle - DocLayNet validation split

    Format: JSON (COCO-style annotations)

    Purpose: Test document layout analysis and region detection

3. ICDAR 2013 - Text OCR Baseline

    Source: Synthetic placeholder dataset

    Format: JSON with text lines and bounding boxes

    Purpose: Establish baseline for pure text OCR accuracy

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


