# 00. ARCHIVE INDEX (V1.0)

## Purpose: Historical Reference

**Status**: ARCHIVED (Superseded by V2.0 in `project_plan/`)
**Created**: 2026-01-31 (Early stages)
**Superseded By**: Concrete documents in `project_plan/`

---

## What's Here

This folder contains the **initial conceptual documentation** created during the early brainstorming phase. These documents were foundational but lacked the specificity needed for production deployment.

### Strategic Overview (Initial)
- **[01_overview.md](01_overview.md)** - Basic solution outline (4-engine architecture concept)
- **[02_roadmap.md](02_roadmap.md)** - Generic 4-phase timeline (week-by-week structure)
- **[03_feature_scalability.md](03_feature_scalability.md)** - Early semantic mapping ideas

### Technical Concepts (Preliminary)
- **[04_functional_specifications.md](04_functional_specifications.md)** - Conceptual module design
- **[05_project_execution_plan.md](05_project_execution_plan.md)** - Generic execution approach

### Analysis Documents
- **[06_critical_review_feasibility.md](06_critical_review_feasibility.md)** - Gap identification (led to V2.0 improvements)
- **[07_validation_proof_strategy.md](07_validation_proof_strategy.md)** - Early validation framework
- **[08_performance_scale_architecture.md](08_performance_scale_architecture.md)** - Initial scale architecture concepts

---

## Why These Were Superseded

### Lack of Specificity

**Example Problems**:
- **Tool Ambiguity**: "Use PaddleOCR" → No version, no installation method
- **Data Vagueness**: "Test on Annual Reports" → No source URLs, no specific companies
- **Performance Claims**: "It will be fast" → No benchmarks, no hardware specs
- **Validation Theory**: "We will test" → No concrete test plan, no success criteria

### V2.0 Improvements

These gaps led to the creation of **3 new concrete documents**:

1. **[05_concrete_data_sources.md](../project_plan/05_concrete_data_sources.md)** ⭐
   - Exact tool versions (PaddleOCR 2.7.3)
   - BSE India URLs with specific CINs
   - GeM hardware specs with prices

2. **[07_performance_benchmarks.md](../project_plan/07_performance_benchmarks.md)** ⭐
   - Industry SLAs (6 min/report)
   - Hardware sizing (₹28.4L cluster)
   - Energy consumption calculations

3. **[08_real_world_validation.md](../project_plan/08_real_world_validation.md)** ⭐
   - 25-report test corpus
   - Ground truth creation method
   - 15-minute demo script

---

## Confidence Score Evolution

| Criterion | V1.0 (Inception) | V2.0 (Project Plan) | Improvement |
|:----------|:-----------------|:--------------------|:------------|
| Government-Centric | 90% | **95%** | +5% |
| Scalable | 70% | **90%** | +20% |
| Performant | 70% | **95%** | +25% |
| Real-World Proof | 60% | **90%** | +30% |
| India-Centric | 95% | **98%** | +3% |
| Secure | 85% | **95%** | +10% |

**Overall**: 75% → **94%** (+19 points)

---

## What's Still Valuable Here

### Conceptual Foundation
- Initial problem analysis
- 4-engine architecture concept
- Phased execution thinking

### Gap Analysis
- `06_critical_review_feasibility.md` identified the gaps that V2.0 addressed
- Honest risk assessment

### Evolution Reference
- Shows how the solution matured from concept to concrete plan
- Demonstrates iterative improvement

---

## How to Use This Folder

### For Team Members
**Purpose**: Understand the evolution of thinking
**Don't Use**: For implementation (use `project_plan/` instead)

### For Documentation
**Purpose**: Show progress in proposal (optional)
**Example**: "We identified gaps in our initial approach and created V2.0 with concrete specifications"

### For Historical Context
**Purpose**: Track decision changes
**Example**: Why did we choose Qdrant over Milvus? (Check evolution of vector DB choices)

---

## Migration Map (V1.0 → V2.0)

| V1.0 Document (Inception) | Superseded By (Project Plan) |
|:--------------------------|:-----------------------------|
| [01_overview.md](01_overview.md) | [01_readme_first.md](../project_plan/01_readme_first.md) (more concrete) |
| [02_roadmap.md](02_roadmap.md) | [08_real_world_validation.md](../project_plan/08_real_world_validation.md) (executable plan) |
| [04_functional_specifications.md](04_functional_specifications.md) | [05_concrete_data_sources.md](../project_plan/05_concrete_data_sources.md) (specific tools) |
| [05_project_execution_plan.md](05_project_execution_plan.md) | [08_real_world_validation.md](../project_plan/08_real_world_validation.md) (test plan) |
| [07_validation_proof_strategy.md](07_validation_proof_strategy.md) | [08_real_world_validation.md](../project_plan/08_real_world_validation.md) (complete) |
| [08_performance_scale_architecture.md](08_performance_scale_architecture.md) | [07_performance_benchmarks.md](../project_plan/07_performance_benchmarks.md) (benchmarks) |

---

## Key Lessons Learned

### Lesson 1: Specificity Matters
**Generic**: "We will use OCR"
**Concrete**: "PaddleOCR Version 2.7.3, Apache 2.0 license, install via pip"

### Lesson 2: Free Sources Are Critical
**Generic**: "Test on Annual Reports"
**Concrete**: "Download from BSE India (https://www.bseindia.com), Reliance CIN: L17110MH1973PLC019786"

### Lesson 3: Government Needs Standards
**Generic**: "We comply with security"
**Concrete**: "Cert-In audit logs: 7 mandatory fields, 90-day retention, write-only table"

### Lesson 4: Proof Over Promise
**Generic**: "It will be accurate"
**Concrete**: "CER <2%, Field Accuracy >95%, tested on 25 reports"

---

## File Summary

| File | Status | Superseded By |
|:-----|:-------|:--------------|
| [01_overview.md](01_overview.md) | ⚠️ BASIC | [01_readme_first.md](../project_plan/01_readme_first.md) |
| [02_roadmap.md](02_roadmap.md) | ⚠️ GENERIC | [08_real_world_validation.md](../project_plan/08_real_world_validation.md) |
| [03_feature_scalability.md](03_feature_scalability.md) | ⚠️ CONCEPTUAL | [04_tech_stack_architecture.md](../project_plan/04_tech_stack_architecture.md) |
| [04_functional_specifications.md](04_functional_specifications.md) | ⚠️ THEORETICAL | [05_concrete_data_sources.md](../project_plan/05_concrete_data_sources.md) |
| [05_project_execution_plan.md](05_project_execution_plan.md) | ⚠️ ABSTRACT | [08_real_world_validation.md](../project_plan/08_real_world_validation.md) |
| [06_critical_review_feasibility.md](06_critical_review_feasibility.md) | ✅ VALUABLE | (Led to V2.0 creation) |
| [07_validation_proof_strategy.md](07_validation_proof_strategy.md) | ⚠️ INCOMPLETE | [08_real_world_validation.md](../project_plan/08_real_world_validation.md) |
| [08_performance_scale_architecture.md](08_performance_scale_architecture.md) | ⚠️ NO BENCHMARKS | [07_performance_benchmarks.md](../project_plan/07_performance_benchmarks.md) |

---

**Recommendation**: Use `project_plan/` folder for all implementation work. This folder is for reference only.
