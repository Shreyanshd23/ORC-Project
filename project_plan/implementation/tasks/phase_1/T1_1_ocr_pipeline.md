# TASK: PHASE 1 - THE VISION LAYER: T1.1 OCR PIPELINE

**Status**: [IN_PROGRESS] 🏗️
**Objective**: Implement the OCR processing engine using Docling. This task focuses solely on the **Implementation** of the wrapper and CLI. Validation will handle in T1.4.
**Ownership**: Engineering Team  
**Tooling**: `Docling` (Primary), `PaddleOCR` (Underlying)

---

## T1.1: OCR PIPELINE IMPLEMENTATION
**Objective**: Build and functionalize the code required to process a PDF.

### **Action Steps**:
1. [x] Research and select the primary OCR engine (Docling selected).
2. [x] Implement a `src/vision/ocr_engine.py` wrapper.
3. [x] Add dependencies (`docling`, `pymupdf`).
4. [x] Create a CLI entry point `src/vision/main.py`.
5. [x] **Refine Wrapper**: clean API exposed (`process_pdf`) for consumption by T1.4 script.

### **Files Affected**:
- `src/vision/ocr_engine.py` (Implementation)
- `src/vision/main.py` (CLI)

### **Validation**:
- [x] Code runs without syntax errors.
- [x] `src/vision/main.py` accepts input flags.
- [ ] Engine produces *some* output (accuracy is not judged here).

---

## PHASE 1 COMPLETION CRITERIA (T1.1 ONLY)
1. Python wrapper `OCREngine` is importable and callable.
2. CLI tool works on a sample file.
