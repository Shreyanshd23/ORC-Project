# Financial Document Accuracy Evaluation (Enhanced Version)

An advanced, recursive metric system for evaluating the accuracy of OCR-extracted financial document content. This version provides comprehensive accuracy metrics including numeric precision, line item matching, section presence, and disclosure statement verification.

## Overview

This module implements a sophisticated evaluation framework that recursively traverses ground truth JSON structures to extract all numbers and text content, then compares them against OCR output using multiple specialized metrics.

## Core Functions

### Text Normalization

#### `normalize_text(text: str) -> str`
Normalizes text by converting to lowercase and collapsing whitespace for consistent matching.

#### `normalize_number(n: str) -> str`
Cleans number strings by removing everything except digits, decimal points, and minus signs.

### Recursive Extraction Functions

#### `extract_all_numbers(obj: Any) -> List[str]`
Recursively traverses any JSON-like structure (dicts, lists, strings, numbers) to extract all numeric values.

**Supported input types:**
- Dictionaries: Recursively processes all values
- Lists: Recursively processes all items
- Strings: Extracts numbers using regex pattern `-?\d[\d,\.]*`
- Integers/Floats: Converts directly to strings

#### `extract_all_text(obj: Any) -> List[str]`
Recursively traverses any JSON-like structure to extract all text strings.

**Supported input types:**
- Dictionaries: Recursively processes all values
- Lists: Recursively processes all items
- Strings: Returns stripped non-empty strings

## Main Function

### `financial_accuracy_report(gt_json: Dict[str, Any], ocr_text: str) -> Dict[str, Any]`

Computes comprehensive financial accuracy metrics by comparing ground truth data with OCR-extracted text.

**Parameters:**
- `gt_json` (*Dict[str, Any]*): Ground truth data in any nested JSON format (tables, sections, metadata)
- `ocr_text` (*str*): OCR-extracted text from the document

**Returns:**
- *Dict[str, Any]*: Dictionary containing four accuracy metrics and a weighted overall score

## Accuracy Metrics

### 1. Numeric Accuracy (40% weight)
Evaluates how well numbers are preserved in the OCR output.

**Calculation:**
- Recursively extracts all numbers from ground truth JSON
- Normalizes numbers (removes formatting characters)
- Counts how many unique ground truth numbers appear in OCR text
- Returns `matched_numbers / total_numbers`

### 2. Line Item Accuracy (20% weight)
Measures how many text labels/descriptions are correctly extracted.

**Calculation:**
- Recursively extracts all text strings from ground truth JSON
- Filters out very short strings (length ≤ 3 characters)
- Normalizes text (lowercase, collapsed whitespace)
- Counts how many text items appear in normalized OCR text
- Returns `matched_items / total_items`

### 3. Section Accuracy (20% weight)
Checks for presence of mandatory financial sections.

**Required sections checked:**
- "balance sheet"
- "statement of profit and loss"
- "cash flow"
- "auditor"

**Calculation:** `matched_sections / 4`

### 4. Disclosure Accuracy (20% weight)
Verifies presence of standard financial disclosure statements.

**Disclosure keywords checked:**
- "true and fair"
- "for the year ended"
- "earnings per equity share"
- "as at march"

**Calculation:** `matched_disclosures / 4`

### Final Overall Score
Weighted combination of all four metrics:
final_score = (
numeric_accuracy * 0.4 +
line_item_accuracy * 0.2 +
section_accuracy * 0.2 +
disclosure_accuracy * 0.2
)

# Key Features
✅ Recursive Extraction

    Automatically traverses deeply nested JSON structures

    Works with any combination of dictionaries, lists, and primitive types

    No assumptions about data structure required

✅ Intelligent Text Filtering

    Filters out very short strings (≤ 3 chars) to avoid false positives

    Removes empty or whitespace-only strings

✅ Robust Number Handling

    Handles formatted numbers with commas and decimal points

    Preserves negative numbers with minus sign

    Normalizes for consistent matching

✅ Weighted Scoring

    Numeric accuracy given highest weight (40%) as it's most critical

    Other metrics equally weighted (20% each)

    Final score provides single metric for overall quality

# Dependencies

    Python 3.6+

    Standard library modules: re, typing

# Notes and Limitations
## Strengths

    Format-agnostic: works with any JSON structure

    Recursive extraction ensures no data is missed

    Multiple metrics provide comprehensive evaluation

## Limitations

    Line item matching is exact and case-insensitive only

    Section/disclosure detection is keyword-based (no semantic understanding)

    Numbers must appear exactly as in ground truth (after normalization)

    Short text strings (≤ 3 chars) are ignored to reduce noise

## Best Practices

    Ensure ground truth JSON contains all relevant financial data

    Include both numeric values and their labels/descriptions

    Use consistent formatting in ground truth for best results

    Include section headers and disclosure statements explicitly in ground truth

