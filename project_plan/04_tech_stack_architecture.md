# 04. TECHNOLOGY STACK & ARCHITECTURE STRATEGY

## Executive Summary
This document defines the **100% Open Source ("FOSS")** technology choices for the AI-FRC "Digital Auditor".

**The Strategic USP**: **"Zero Vendor Lock-in, Zero Licensing Costs."**
Unlike competitors building "wrappers" around expensive APIs (OpenAI/Google), our solution is a **Sovereign Asset**. It runs entirely on NFRA's own hardware, incurring only compute costs (electricity/GPUs), with no per-page or per-user subscription fees.

---

## The Tech Stack: "Sovereign & Cost-Efficient"

### 1. The Core Engines (Backend & Logic)
*   **Language**: **Python 3.11+** (Open Source)
    *   *Role*: Universal glue code.
*   **API Framework**: **FastAPI** (License: MIT)
    *   *Why*: High-performance, community-driven, and lightweight.
*   **Orchestration**: **LangGraph** (License: MIT)
    *   *Why*: Allows us to build complex "Agentic Loops" (cyclic logic) without paying for proprietary orchestration platforms like stack-specific enterprise tools.

### 2. The Vision Layer (Free & Customisable OCR)
Instead of paying AWS Textract ($1.50/1000 pages) or Azure Form Recognizer, we deploy state-of-the-art Open Source models.

*   **PDF Parsing**: **Docling** (IBM Open Source - MIT)
    *   *Why*: Breaks away from the "Text streams" paradigm. It treats documents as structured data (JSON) directly, handling multi-column layouts better than pypdf.
*   **OCR Engine**: **PaddleOCR** (Apache 2.0)
    *   *Why*: The current SOTA (State of the Art) for lightweight OCR. Supports 80+ languages including Hindi/Devanagari (critical for Indian context).
    *   *Cost*: **₹0**.
*   **Table Extraction**: **Surya** (GPL-3.0) or **Table Transformer** (Microsoft - MIT)
    *   *Why*: Specialized vision models that detecting table borders and structures visually, rather than relying on PDF metadata (which is often broken).

### 3. The "Brain" (Open Weights LLM)
We prove that "Open" is now "Better" than "Closed" for specialized tasks.

*   **LLM**: **Mistral-Large-2** or **Llama-3-70B** (Open Weights)
    *   *Deployment*: **vLLM** (Apache 2.0).
    *   *Why*: High-throughput local serving.
    *   *Customizability*: Crucially, **we can Fine-Tune these**. We can take 500 past NFRA Audit Reports and train Llama-3 to speak "Auditor" perfectly. You cannot deeper fine-tune GPT-4 architecture.
*   **Protocol**: **Ollama** (MIT) for easy local development and inference handoffs.

### 4. The Memory (No Enterprise Licenses)
*   **Vector Database**: **Qdrant** (Apache 2.0) or **Milvus** (Apache 2.0)
    *   *Why*: Pure open-source vector search. Qdrant is Rust-based (extremely fast/efficient), reducing hardware costs compared to Java-based alternatives.
*   **Database**: **PostgreSQL** (PostgreSQL License - Freedom)
    *   *Why*: The gold standard. No "Enterprise Edition" features walled off.
*   **Object Storage**: **MinIO** (AGPL v3)
    *   *Why*: S3-compatible storage that runs on any cheap server. No AWS bills.

### 5. The Face (Community Standard)
*   **Framework**: **Next.js** (MIT)
    *   *Why*: The largest developer ecosystem on earth. Hiring maintainers is easy.
*   **Search**: **SearXNG** (AGPL)
    *   *Why*: For the "Preliminary Examination Tool". Instead of paying for Bing API, we perform meta-searches across public indexes without tracking.
*   **Compliance (UI/UX)**: **GIGW 3.0 Compliance**
    *   *Why*: Mandatory for all Indian Government portals. Ensures WCAG 2.1 accessibility standards and a standardized user experience across NIC/CDAC environments.

---

## The "Cost & Freedom" Analysis

This table defines our USP in the "Deep Tech" Pitch.

| Feature | Competitor (API Wrapper) | Our Solution (Open Source) | **The "Nitty-Gritty" Advantage** |
| :--- | :--- | :--- | :--- |
| **Data Privacy** | **Zero**. Data sent to US servers (OpenAI/Azure). | **100% Sovereign**. Data never leaves the machine. | Complies strictly with the **Digital Personal Data Protection (DPDP) Act 2023**. |
| **Cost** | **₹20-₹50 per Annual Report** (Token costs). | **₹0**. (Marginal electricity cost). | **Scalability is Free**. Processing 1 million documents costs the same infrastructure, not 1 million x API Fees. |
| **Accuracy** | General Purpose (Good at poems, okay at math). | **Fine-Tunable**. | We can train the model specifically on *Indian Accounting Standards (IndAS)*. |
| **Vendor Risk** | High. If OpenAI bans the account, the Govt tool stops. | **Zero**. We own the weights. | The solution will work in 2030 exactly as it does today, referencing the same container images. |
| **Search** | Google Custom Search API ($5/1000 queries). | **SearXNG**. | Unlimited queries for background checks on companies. |

---

## Why "Open" is "Compliance-Ready"

1.  **Auditable Code**: The NFRA technical team can read every line of our code. There are no "black boxes".
2.  **Long-Term Archiving**: Proprietary APIs change versions and deprecate features. Our Docker containers can be archived for 10 years and will still spin up to audit a 2026 report in 2036.
3.  **Community Security**: Open source libraries (like LangChain, FastAPI) are patched by thousands of contributors worldwide, often faster than proprietary patches.

---

## Implementation Prerequisites Check

Before writing a single line of code, we must lock these documents:
1.  **Functional Specification (FSD)**: defining the exact JSON schema for the "Compliance Report".
2.  **Regulatory Map (The "Truth")**: A standardized mapping of IndAS sections to "Search Queries".
3.  **Security Protocol**: Defining how we handle PII (Directors' PAN numbers, Signatures) extracted from reports.
