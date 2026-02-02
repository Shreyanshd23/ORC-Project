# EXECUTION ROADMAP & DEPENDENCY GRAPH

This document defines the strictly ordered execution sequence for the AI-FRC "Digital Auditor". Tasks are grouped by **Blocking Sync** (must wait) and **Parallel Async** (can happen at the same time).

---

## Phase 0: Ground Zero (Day 0 - Day 3)
*Goal: Infrastructure, Scaffolding & Fallback Readiness*

| ID | Task Name | Type | Dependency |
|:---|:---|:---|:---|
| T0.1 | **Project Scaffolding** (Repo init, Folder structure, Docker boilerplate) | Blocking | None |
| T0.2 | **Environment & Fallback** (Setup CPU-first env; GPU drivers as "upgrade") | Blocking | T0.1 |
| T0.3 | **Global Dataset Alignment** (Acquire FinTabNet/DocLayNet/OmniDocBench) | Blocking | None |
| T0.4 | **Benchmark Data Pull** (Download 25 Target Reports from BSE India) | Blocking | None |
| T0.5 | **Ground Truth Creation** (Manual Excel extraction of Reliance/Tata/BHEL) | Parallel | T0.4 |

---

## Phase 1: The Vision Layer (Week 1 - Week 2)
*Goal: Convert unstructured PDFs into high-fidelity structured JSON*

| ID | Task Name | Status | Dependency |
|:---|:---|:---|:---|
| T1.1 | **OCR Pipeline** (Docling Integration) | [IN_PROGRESS] | T0.2 |
| T1.4 | **Base Engine Validation** (Benchmark CER/F1) | [IN_PROGRESS] | T1.1 |
| T1.2 | **Document Structure Mapper** (Segmenting Sections) | [PAUSED] | T1.4 |
| T1.3 | **Table Extraction Engine** (Docling/Surya) | [TODO] | T1.2 |
| T1.5 | **Real-World Adaptation** (Fine-tuning for BSE Reports) | [TODO] | T1.4 |
| T1.6 | **Final Accuracy Test** (Check against Ground Truth) | [TODO] | T1.5 |

---

## Phase 2: The Logic Engine (Week 3 - Week 4)
*Goal: Transform extracted data into compliance verdicts*

| ID | Task Name | Type | Dependency |
|:---|:---|:---|:---|
| T2.1 | **Schema Standardization** (Convert all extracted items to unified IndAS JSON) | Blocking | T1.3 |
| T2.2 | **Rule-Set Implementation** (Codifying 10 high-prio objective IndAS rules) | Blocking | T2.1 |
| T2.3 | **Financial Analytics Engine** (Ratio calculations, CY vs PY drifts) | Parallel | T2.1 |
| T2.4 | **Regulatory Knowledge Base** (Parsing IndAS PDFs into vector embeddings) | Parallel | T0.1 |

---

## Phase 3: The Insight Layer (Week 5 - Week 6)
*Goal: Conversational interface and automated reporting*

| ID | Task Name | Type | Dependency |
|:---|:---|:---|:---|
| T3.1 | **Insight Bot (RAG)** (Citation-backed Q&A for "Notes to Accounts") | Blocking | T2.4, T1.1 |
| T3.2 | **Compliance Report Generator** (Auto-generation of PDF/Word audit summary) | Blocking | T2.2 |
| T3.3 | **Frontend Development** (GIGW 3.0 Dashboard, Search, PDF Viewer) | Parallel | T2.2 |

---

## Phase 4: Hardening & Compliance (Week 7)
*Goal: Security audits and GIGW compliance*

| ID | Task Name | Type | Dependency |
|:---|:---|:---|:---|
| T4.1 | **PII Redaction Pipeline** (Ensuring PAN/Aadhaar/Signs are protected) | Blocking | T3.1 |
| T4.2 | **GIGW 3.0 Accessibility Audit** (WCAG 2.1 check on UI) | Blocking | T3.3 |
| T4.3 | **Performance Tuning** (Optimizing vLLM batching for 6 min/report target) | Parallel | T3.1 |
| T4.4 | **Self-VAPT Audit** (Internal vulnerability scan before 3rd party) | Parallel | T3.3 |

---

## Phase 5: Final Validation & Demo (Week 8)
*Goal: Judges' ready state*

| ID | Task Name | Type | Dependency |
|:---|:---|:---|:---|
| T5.1 | **Load Testing** (Locust test for 100 concurrent uploads) | Blocking | T4.3 |
| T5.2 | **Demo Script Finalization** (Revisiting the 15-min judge's flow) | Blocking | All |
| T5.3 | **External VAPT Certification** ("Safe-to-Host" by empanelled auditor) | Parallel | T4.4 |
| T5.4 | **Training Materials** (User manuals in English/Hindi) | Parallel | T3.3 |

---

## Critical Dependency Flow
1. **Infrastructure (T0.1)** → **OCR (T1.1)** → **Extraction (T1.3)** → **Rules (T2.2)** → **Report (T3.2)**.
2. **Standardization (T2.1)** acts as the "Grand Bridge" between Vision and Logic.
3. **UI (T3.3)** and **Rules (T2.2)** must converge by Week 6 to show a demo-able product.
