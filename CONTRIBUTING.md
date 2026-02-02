# Contributing Guidelines

**⚠ STRICTLY CONFIDENTIAL & PROPRIETARY ⚠**

This repository contains proprietary source code and intellectual property belonging to **Exascale Deeptech and AI Private Ltd.**  
([https://exascale-ai.com/](https://exascale-ai.com/))

Unauthorized copying, distribution, modification, public display, or use of this file or any part of the software, via any medium, is strictly prohibited.

---

## 1. Access & Authorization
Access to this repository is granted strictly on a **Need-to-Know basis** to:
*   Full-time employees of Exascale Deeptech and AI Private Ltd.
*   Contractors and partners with active Non-Disclosure Agreements (NDAs) and specific written authorization.

If you have stumbled upon this repository by accident, you must disconnect immediately and notify `tech@exascale-ai.com`.

## 2. Development Standards
To maintain industry-grade quality and security, all contributors must adhere to the following:

### A. Security First
*   **NEVER** commit API keys, passwords, or production secrets. Use `.env` files (which are `.gitignore`'d).
*   **NEVER** upload internal datasets (PDFs, JSONs) to public forums, Gists, or unauthorized cloud storage.
*   All data processing must run **LOCALLY** or within the designated air-gapped environment (as per `src/vision/ocr_engine.py` configurations).

### B. Contribution Workflow
1.  **Ticket-Based Work**: No code is written without a corresponding Task ID from the Roadmap.
2.  **Branching Strategy**:
    *   `main`: Production-ready code. Locked.
    *   `dev`: Integration branch.
    *   `feat/T1-OCR-Engine`: Feature branches named after Task IDs.
3.  **Pull Requests**:
    *   Must generally pass all local benchmarks (`scripts/benchmark_ocr.py`).
    *   Must be reviewed by at least one Senior Engineer.

## 3. Intellectual Property
By contributing to this repository, you acknowledge that:
1.  All code, documentation, and assets created are the **sole property of Exascale Deeptech and AI Private Ltd.** and are "Works Made for Hire" under applicable law.
2.  You waive any moral rights to the code contributed.

## 4. Reporting Vulnerabilities
If you discover a security vulnerability, **DO NOT** create a public Issue.
Report it directly to the CTO or Security Lead via internal encrypted channels.

---

**© 2026 Exascale Deeptech and AI Private Ltd. All Rights Reserved.**
