# Compliance Rules Validation

A simple rule-based compliance checker for financial documents that validates the presence of required sections and detects specific tables in OCR-extracted text.

## Overview

This module provides functionality to validate whether key financial sections and tables are present in an OCR-processed document. It performs case-insensitive text matching to verify compliance with reporting requirements.

## Function

### `validate_compliance(gt_json: dict, ocr_text: str)`

Validates document compliance by checking for required sections and tables in the OCR text.

**Parameters:**
- `gt_json` (*dict*): Ground truth JSON containing document structure information, expected to have:
  - `tables`: List of table objects, each with a `title` field
- `ocr_text` (*str*): OCR-extracted text from the document

**Returns:**
- *List[Dict]*: List of validation results, each containing:
  - `rule`: Description of the compliance rule being checked
  - `status`: Either "PASS" (rule satisfied) or "FAIL" (rule violated)

## Compliance Rules Checked

### Required Sections
The function checks for the presence of these mandatory sections (case-insensitive):
- "balance sheet"
- "statement of profit and loss"
- "cash flow"
- "auditor"

### Table Detection
For each table defined in the ground truth JSON, the function verifies that its title appears in the OCR text.

## Usage Example

```python
# Ground truth JSON with table information
gt_json = {
    "tables": [
        {"title": "Annual Balance Sheet 2023"},
        {"title": "Cash Flow Statement"}
    ]
}

# OCR extracted text
ocr_text = """
The balance sheet shows total assets of $1.2M.
The statement of profit and loss indicates revenue growth.
Cash flow from operations was positive.
Auditor: PriceWaterhouseCoopers.
Annual Balance Sheet 2023 is attached below.
"""

# Validate compliance
results = validate_compliance(gt_json, ocr_text)

for result in results:
    print(f"{result['rule']}: {result['status']}")

# Output:
# Balance Sheet Present: PASS
# Statement Of Profit And Loss Present: PASS
# Cash Flow Present: PASS
# Auditor Present: PASS
# Table Detected: Annual Balance Sheet 2023: PASS
# Table Detected: Cash Flow Statement: FAIL
```
# Return Value Structure
```python
Each result in the returned list follows this format:
python

{
    "rule": str,      # Description of the rule being checked
    "status": str     # "PASS" or "FAIL"
}
```
# Limitations

    Simple string matching only (no semantic understanding)

    Case-insensitive but requires exact substring match

    No handling of typos or variations in section names

    Does not validate content quality, only presence

    Table detection only checks titles, not table content

# Dependencies

    Python 3.6+

    No external dependencies

# Notes

    The function performs case-insensitive matching by converting both the OCR text and search terms to lowercase

    Table validation only occurs if the tables key exists in gt_json

    Empty table titles are skipped during validation