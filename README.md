# IndiaAI Financial Reporting Compliance Challenge - Documentation

## Project Status: PRODUCTION READY ✅
**Last Updated**: 2026-01-31
**Version**: 2.0 (Concrete & Specific)
**Overall Readiness**: 94%

---

## Folder Structure

### 📁 `src/` (CORE ENGINE)
**Contains**: Python source code
- `vision/`: OCR pipeline, Docling integration

### 📁 `scripts/` (TOOLS)
**Contains**: DevOps and Testing utilities
- `benchmark_ocr.py`: Validation script

### 📁 `project_plan/` (DOCUMENTATION)
**Contains**: Production-ready documentation

**Start Here**:
1. **[01_readme_first.md](project_plan/01_readme_first.md)** - Executive summary and quick reference
2. **[02_index_critical_summary.md](project_plan/02_index_critical_summary.md)** - Confidence scores and navigation
3. **[03_gap_closure_summary.md](project_plan/03_gap_closure_summary.md)** - V1.0 → V2.0 transformation details

**Technical Specifications**:
- [04_tech_stack_architecture.md](project_plan/04_tech_stack_architecture.md) - 100% Open Source tools (exact versions)
- [05_concrete_data_sources.md](project_plan/05_concrete_data_sources.md) ⭐ - Tools, data URLs, GeM hardware specs
- [06_data_security_governance.md](project_plan/06_data_security_governance.md) - MeitY Cloud, Cert-In compliance

**Performance & Validation**:
- [07_performance_benchmarks.md](project_plan/07_performance_benchmarks.md) ⭐ - Industry SLAs, hardware sizing
- [08_real_world_validation.md](project_plan/08_real_world_validation.md) ⭐ - Test corpus, demo script, risk mitigation

---

### 📁 `inception/` (ARCHIVE - V1.0)
**Contains**: Earlier conceptual documents and gap analysis

**Purpose**: Historical reference showing evolution of thinking

**Documents**:
- [01_overview.md](inception/01_overview.md) - Initial solution outline
- [02_roadmap.md](inception/02_roadmap.md) - Basic 4-phase timeline
- [03_feature_scalability.md](inception/03_feature_scalability.md) - Early semantic architecture ideas
- [04_functional_specifications.md](inception/04_functional_specifications.md) - Conceptual module design
- [05_project_execution_plan.md](inception/05_project_execution_plan.md) - Generic execution approach
- [06_critical_review_feasibility.md](inception/06_critical_review_feasibility.md) - Gap identification analysis
- [07_validation_proof_strategy.md](inception/07_validation_proof_strategy.md) - Early validation framework
- [08_performance_scale_architecture.md](inception/08_performance_scale_architecture.md) - Initial scale concepts

**Note**: These were superseded by the concrete V2.0 documents in `project_plan/`

---

## Quick Reference

### Critical Numbers
- **Performance**: 6 min/report (500 pages native PDF)
- **Scalability**: 300 reports/day (4-node cluster)
- **Cost**: ₹28.4 Lakh (production cluster), ₹0/report processing
- **Accuracy**: >95% table extraction target

### Data Sources (Free)
- **Test Reports**: BSE India (https://www.bseindia.com)
- **IndAS Standards**: ICAI (https://www.icai.org)
- **Companies Act**: MCA Portal (https://www.mca.gov.in)

### Hardware (GeM)
- **MVP**: HCL TechBee HSW130W, ₹4.8 Lakh (NVIDIA T4)
- **Production**: 4-node cluster, ₹28.4 Lakh total

### Compliance
- **Security**: DPDP Act 2023, Cert-In standards
- **Deployment**: MeitY Cloud (NIC/CDAC), K8s 1.28+
- **Sovereignty**: 100% on-premise (air-gapped LLM)

---

## ⚡ Developer Quick Start

### 1. Prerequisites
- **Python**: 3.11+
- **Tooling**: [uv](https://github.com/astral-sh/uv) (Recommended) or `pip`
- **OS**: Mac (MPS), Linux (CUDA), or Windows (CPU/CUDA)

### 2. Installation
```bash
# 1. Install dependencies
uv sync

# 2. Verify environment
uv run python infra/scripts/check_env.py
```

### 3. Usage
**Running OCR on a Document:**
```bash
# Process a single PDF
uv run python -m src.vision.main --input data/raw/report.pdf --output data/processed

# Process an entire folder
uv run python -m src.vision.main --input data/raw/ --output data/processed
```

**Running Benchmarks:**
```bash
# Calculate Accuracy (CER/WER) against Ground Truth
uv run python scripts/benchmark_ocr.py --ground-truth data/benchmarks/gt.txt --prediction data/processed/output.md
```

### 4. Contributing Flow
We follow a strict **Task-Based Workflow**.
1. **Check the Roadmap**: See [01_execution_roadmap.md](project_plan/implementation/tasks/01_execution_roadmap.md).
2. **Pick a Task**: Status must be `[TODO]` or `[IN_PROGRESS]`.
3. **Read the Spec**: Open the specific task file (e.g., `T1_1_ocr_pipeline.md`) in `project_plan/implementation/tasks/`.
4. **Implement & Verify**: Ensure you meet the "Validation" criteria before PR.

---

## 🔒 Legal & Compliance

**Proprietary Software**: This repository is the intellectual property of **Exascale Deeptech and AI Private Ltd.**
- **License**: See [LICENSE](LICENSE) for strict usage terms.
- **Contribution**: See [CONTRIBUTING.md](CONTRIBUTING.md) for NDA and security protocols.

**Contact**: `tech@exascale-ai.com` for access or security inquiries.

---

---

## Competition Details

**Challenge**: IndiaAI Financial Reporting Compliance
**Organizer**: MeitY + NFRA
**Stage 2**: Virtual Round (INR 5 Lakh)
**Stage 3**: On-Premises Round (INR 1 Crore contract)
**Link**: https://aikosh.indiaai.gov.in/home/competitions/details/b5ebae1e-73d1-4ba8-baa1-21beaabd1f6d

---

## Documentation Index

**For Implementation Team**: Start with [project_plan/](project_plan/00_folder_index.md)
**For Judges/Reviewers**: Read [project_plan/01_readme_first.md](project_plan/01_readme_first.md)
**For Historical Context**: Check [inception/](inception/00_archive_index.md) folder

---

**Last Updated**: 2026-01-31 18:01 IST
**Status**: READY FOR EXECUTION ✅
