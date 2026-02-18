# Docling OCR Engine

A robust OCR engine wrapper for processing PDF documents using the Docling library. This module provides comprehensive PDF processing capabilities including page range selection, text extraction, table detection, and progress tracking.

## Overview

The Docling OCR Engine is designed for high-quality text extraction from financial and business documents. It automatically detects whether a PDF has embedded text and applies OCR only when necessary, optimizing both speed and accuracy.

## Features

- ✅ **Intelligent OCR**: Automatically detects embedded text and applies OCR only when needed
- ✅ **Page Range Processing**: Extract specific page ranges from large documents
- ✅ **Table Extraction**: Detects and structures tables from documents
- ✅ **Progress Tracking**: Real-time progress updates with callback support
- ✅ **PDF Validation**: Checks for corrupted or invalid PDFs
- ✅ **Multi-format Output**: Returns raw text, cleaned text, tables, and markdown
- ✅ **Thread-safe Progress Simulation**: Non-blocking progress updates during long operations

## Dependencies

### External Libraries
- `PyPDF2`: PDF parsing and manipulation
- `docling`: Core OCR and document processing
- Standard library: `time`, `logging`, `threading`, `pathlib`, `typing`, `re`

## Helper Functions

### PDF Validation

#### `is_valid_pdf(pdf_path: str) -> bool`
Checks if a PDF file is valid and not corrupted.

**Parameters:**
- `pdf_path`: Path to the PDF file

**Returns:**
- `True` if PDF can be opened, `False` otherwise

#### `has_embedded_text(pdf_path: str) -> bool`
Detects if the PDF contains selectable/embedded text (as opposed to scanned images).

**Parameters:**
- `pdf_path`: Path to the PDF file

**Returns:**
- `True` if text is found in first 3 pages, `False` otherwise

### PDF Processing

#### `create_temp_pdf(original_path: Path, start_page: int, end_page: int) -> Path`
Creates a temporary PDF containing only the specified page range.

**Parameters:**
- `original_path`: Path to original PDF
- `start_page`: First page to include (1-indexed)
- `end_page`: Last page to include (1-indexed)

**Returns:**
- Path to temporary PDF file (automatically cleaned up after processing)

## OCREngine Class

### Initialization

```python
engine = OCREngine()