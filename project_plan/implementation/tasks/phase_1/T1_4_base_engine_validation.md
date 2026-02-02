# TASK: PHASE 1 - THE VISION LAYER: T1.4 BASE ENGINE VALIDATION

**Status**: [IN_PROGRESS] 📊
**Objective**: Quantitatively measure the reliability of the OCR engine on general and base-line documents to ensure a stable foundation for Phase 2.
**Ownership**: Engineering Team  
**Tooling**: `docling`, `Levenshtein` (for CER calculation)

---

## T1.4: BASE ENGINE VALIDATION
**Objective**: Establish a benchmark for OCR accuracy (CER/WER) and layout preservation.

### **Action Steps (Intern/Developer)**:

#### **Step 1: Run the Baseline Benchmark**
1.  Ensure you have the "Ground Truth" file: `data/benchmarks/page_61_gt.txt`.
2.  Run the OCR engine on the test PDF:
    ```bash
    uv run python -m src.vision.main --input data/benchmarks/page_61.pdf --output data/benchmarks/results
    ```
3.  Run the Comparison Script:
    ```bash
    uv run python scripts/benchmark_ocr.py --ground-truth data/benchmarks/page_61_gt.txt --prediction data/benchmarks/results/page_61.md
    ```

#### **Step 2: Analyze the Failure (The "Why")**
1.  Open `data/benchmarks/results/page_61.md` in your IDE.
2.  Compare it visually to `data/benchmarks/page_61.pdf`.
3.  **Check**: Does the markdown use a `| Table |` syntax for the "Key Audit Matters" section? Or is it just headers (`##`)?
    *   *Current Failure Mode*: Docling flattens the table into lists. This is failing the benchmark.

#### **Step 3: Tune the Engine (The Fix)**
1.  Edit `src/vision/ocr_engine.py`.
2.  Modify `PipelineOptions` to improve table detection.
    *   Verify `do_cell_matching = True` is active.
    *   Try changing `table_structure_options.mode`.
3.  Re-run Step 1 until you see a Markdown Table in the output.

### **Deliverables (Required for PR)**:
1.  **Console Output**: Screenshot of `benchmark_ocr.py` showing `CER` (don't worry if >10% due to formatting, but must be consistent).
2.  **Artifact**: The generated `page_61.md` file showing a correct Markdown Table structure.

### **Validation**:
- [ ] Script outputs a structured report (e.g., `benchmark_results.json`).
- [ ] Baseline CER is < 2% on clean documents.
    - **Note to Assignee**: If CER is high (>10%) but text looks correct, check for **Layout Artifacts** (e.g., table flattening, unified paragraphs). Do not optimize for whitespace/formatting matching unless critical.

---

## PHASE 1 COMPLETION CRITERIA (T1.4)
1. Automated benchmarking tool.
2. Verified accuracy metrics for at least 3 distinct document types.
3. Confidence threshold reached for moving to "Real-World Adaptation" (T1.5).
