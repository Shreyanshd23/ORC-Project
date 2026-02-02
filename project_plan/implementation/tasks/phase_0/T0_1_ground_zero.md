# TASK: PHASE 0 - GROUND ZERO (SCAFFOLDING & PREREQUISITES)

**Status**: [DONE] ✅
**Objective**: Build the foundational infrastructure, environment, and benchmark datasets required for the Vision Layer (Phase 1).  
**Ownership**: Engineering & Data Team  
**Tooling**: `uv` (Python Package Manager), `Docker`

> **JIT Scaffolding Note**: In this project, we follow a Just-In-Time approach. Directories and files are created ONLY when they are strictly required for the current task. This maintains a clean workspace and avoids placeholder "ghost" folders.

---

## T0.1: PROJECT SCAFFOLDING & INITIALIZATION
**Status**: [DONE] ✅
**Objective**: Establish the root directory structure and source control.

### **Action Steps**:
1. [x] Initialize the project with `uv init AI-FRC`.
2. [x] Configure `.gitignore` to prevent data/model leakage.

### **Files Affected**:
- `pyproject.toml` (Created)
- `.python-version` (Created)
- `.gitignore` (Created)
- `README.md` (Update with project title)

### **Validation**:
- [x] Root files exist.
- [x] `uv --version` returns version > 0.5.0.

---

## T0.2: ENVIRONMENT & FALLBACK (CPU/GPU DETECTOR)
**Status**: [DONE] ✅
**Objective**: Setup a reproducible environment that works on both Mac/CPU and Linux/GPU.

### **Action Steps**:
1. [x] Create `infra/scripts/` and `src/utils/` directories.
2. [x] Add core dependencies via `uv add`.
3. [x] Create a `src/utils/hardware.py` script to detect `CUDA` vs `MPS` vs `CPU`.
4. [x] Create a `infra/scripts/check_env.py` to validate imports.

### **Files Affected**:
- `infra/scripts/` (Created)
- `src/utils/` (Created)
- `src/utils/hardware.py` (Created)
- `infra/scripts/check_env.py` (Created)
- `pyproject.toml` (Dependency updates)

### **Validation**:
- [x] Run `uv run infra/scripts/check_env.py` and get success message.

---

## T0.3: VALIDATION DATASET ACQUISITION
**Status**: [TODO]
**Objective**: Acquire specific "Ground Truth" datasets (PDF + JSON pairs) to strictly validate OCR reliability before processing any real-world reports.

### **Action Steps**:
1. [ ] Download **FinTabNet** sample (Validation split) for table-heavy financial document testing.
2. [ ] Download **DocLayNet** sample for complex layout testing.
3. [ ] Download **ICDAR 2013** (if available) for pure text baseline.
4. [ ] Verify that corresponding Ground Truth JSONs are available and readable.

### **Files Affected**:
- `data/benchmarks/fintabnet/` (To be populated)
- `data/benchmarks/doclaynet/` (To be populated)

### **Validation**:
- [ ] At least 3 pairs of matching `sample.pdf` and `sample.json` exist in `data/benchmarks/`.

---

## T0.4: BENCHMARK DATA PULL (INDIAN CORPUS)
**Status**: [DONE] ✅
**Objective**: Acquire the real-world target documents.

### **Action Steps**:
1. [x] Create `data/raw/` directory.
2. [x] Download 2023-24 Annual Reports for Reliance, BHEL, etc.

### **Files Affected**:
- `data/raw/` (Created)
- `data/raw/reliance_2024.pdf` (Downloaded)
- `data/raw/bhel_2024.pdf` (Downloaded)

### **Validation**:
- [x] PDFs exist in `data/raw/` and are readable.

---

## T0.5: GROUND TRUTH CREATION (MANUAL)
**Status**: [DEFERRED - USER MANUAL] 👤
**Objective**: Create the absolute "Gold Standard" for accuracy measurement.

### **Action Steps**:
1. [ ] Create `data/ground_truth/` directory.
2. [ ] Manually extract the Balance Sheet for Reliance 2024.

### **Files Affected**:
- `data/ground_truth/` (Directory created)
- `data/ground_truth/reliance_2024_gt.json`

### **Validation**:
- [ ] Peer review the JSON against the PDF to ensure 100% manual accuracy.

---

## PHASE 0 COMPLETION CRITERIA
1. The project can be "synced" with a single command: `uv sync`.
2. Hardware detector successfully reports current machine capabilities.
3. At least 1 target report has a corresponding Ground Truth file for T1.4 testing. (Handled manually by User)
