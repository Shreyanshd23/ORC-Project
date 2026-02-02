# TASK: PHASE 1 - THE VISION LAYER: T1.1 OCR PIPELINE

**Status**: [IN_PROGRESS] 🏗️
**Objective**: Implement the OCR processing engine using Docling. This task focuses solely on the **Implementation** of the wrapper and CLI. Validation will handle in T1.4.
**Ownership**: Engineering Team  
**Tooling**: `Docling` (Primary), `PaddleOCR` (Underlying)

---

## T1.1: OCR PIPELINE - PRODUCTION READY
**Objective**: Make the existing Docling-based OCR engine competition-ready with proper configuration, error handling, and optional engine comparison.

### **Current State**:
- ✅ Basic Docling wrapper exists (`src/vision/ocr_engine.py`)
- ✅ CLI tool works (`src/vision/main.py`)
- ❌ Configuration is hardcoded
- ❌ No error handling for corrupted PDFs
- ❌ No alternative engines for comparison

### **Action Steps (Intern/Developer)**:

#### **Step 1: Production-Grade Configuration**
**Goal**: Maximize table extraction accuracy and system reliability.

**Requirements**:
1.  **Table Detection Optimization**: Research and apply the most accurate configuration settings available in the current OCR library for table structure recognition.
2.  **Error Resilience**: The system must gracefully handle corrupted or malformed PDFs without crashing. Failed documents should be logged with error details.
3.  **User Feedback**: For large multi-page documents, provide real-time progress indication (e.g., "Processing page X of Y").

**Success Criteria**:
- System processes a 100-page PDF without crashes
- Corrupted PDFs generate error logs instead of exceptions
- User sees progress updates during processing

#### **Step 2: Engine Comparison Framework**
**Goal**: Validate our choice of OCR engine by comparing it against at least one alternative.

**Requirements**:
1.  **Alternative Engine**: Research and integrate ONE alternative OCR engine known for speed or accuracy. Document your selection rationale.
2.  **Isolation**: Each engine should be callable independently - no complex orchestration needed at this stage.
3.  **Fair Comparison**: Both engines should process the same test document under identical conditions.

**Success Criteria**:
- Two engines can be run via command-line selection
- Both produce comparable output formats (text/markdown)
- Performance metrics (speed, accuracy) are measurable

#### **Step 3: CLI Flexibility**
**Goal**: Make the tool configurable without code changes.

**Requirements**:
1.  **Engine Selection**: Users should be able to choose which OCR engine to use via command-line flag.
2.  **Output Format Control**: Support multiple output formats (at minimum: markdown and JSON).
3.  **Documentation**: Update README with usage examples for all supported configurations.

**Success Criteria**:
- `--help` flag shows all available options
- Same PDF can be processed with different engines using different commands
- Output format can be controlled via CLI flag

### **Deliverables (Required for Competition)**:
1.  **Robust System**: 
    - Handles edge cases (corrupted files, very large documents)
    - Provides clear error messages
    - Shows processing progress
    
2.  **Comparison Analysis**: A document comparing the engines on these dimensions:
    - Processing speed (pages per second)
    - Table detection capability (visual comparison on sample pages)
    - Text accuracy (qualitative assessment)
    - Resource usage (memory, CPU)
    
3.  **Demo Evidence**: 
    - Screen recording showing both engines processing the same document
    - Side-by-side comparison of outputs
    - CLI usage demonstration

### **Validation**:
- [x] Code runs without syntax errors.
- [x] `src/vision/main.py` accepts input flags.
- [ ] Engine produces *some* output (accuracy is not judged here).

---

## PHASE 1 COMPLETION CRITERIA (T1.1 ONLY)
1. Python wrapper `OCREngine` is importable and callable.
2. CLI tool works on a sample file.
