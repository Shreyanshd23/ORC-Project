# TASK: PHASE 1 - THE VISION LAYER: T1.4 BASE ENGINE VALIDATION

**Status**: [IN_PROGRESS] 📊
**Objective**: Quantitatively measure the reliability of the OCR engine on general and base-line documents to ensure a stable foundation for Phase 2.
**Ownership**: Engineering Team  
**Tooling**: `docling`, `Levenshtein` (for CER calculation)

---

## T1.4: BASE ENGINE VALIDATION
**Objective**: Establish a benchmark for OCR accuracy (CER/WER) and layout preservation.

### **Action Steps**:
1. [ ] **Load Ground Truth**: Read the PDF+JSON pairs acquired in T0.3 (`data/benchmarks/`).
2. [ ] **Develop Benchmark Script**: Create `scripts/benchmark_ocr.py` that:
    - Runs the `OCREngine` (from T1.1) on the PDF.
    - Normalizes text (whitespace, casing) for fair comparison.
    - Calculates CER/WER against the T0.3 JSON Ground Truth.
3. [ ] **Execute & Report**: Run on FinTabNet/DocLayNet samples and print a score.

### **Files Affected**:
- `scripts/benchmark_ocr.py` (New script)
- `data/benchmarks/` (Input source from T0.3)

### **Validation**:
- [ ] Script outputs a structured report (e.g., `benchmark_results.json`).
- [ ] Baseline CER is < 2% on clean documents.
    - **Note to Assignee**: If CER is high (>10%) but text looks correct, check for **Layout Artifacts** (e.g., table flattening, unified paragraphs). Do not optimize for whitespace/formatting matching unless critical.

---

## PHASE 1 COMPLETION CRITERIA (T1.4)
1. Automated benchmarking tool.
2. Verified accuracy metrics for at least 3 distinct document types.
3. Confidence threshold reached for moving to "Real-World Adaptation" (T1.5).
