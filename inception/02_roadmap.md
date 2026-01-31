# 02. PROJECT ROADMAP (INCEPTION)

## Phase 1: Foundation & The "Structure Mapper" (Weeks 1-2)
**Goal**: Build the core ingestion engine capable of understanding the anatomy of an Annual Report.

*   **Task 1.1: Multi-Format Ingestion Pipeline**
    *   Implement OCR (Optical Character Recognition) for scanned PDFs.
    *   Develop the **Semantic Structure Mapper** to segment documents into 5 key zones:
        1.  Corporate Identity
        2.  Independent Auditor's Report
        3.  Financial Statements (BS, P&L, Cash Flow)
        4.  Corporate Governance Report
        5.  ESG / BRSR
*   **Task 1.2: Table Extraction Engine**
    *   Deploy deep-learning models (e.g., Table Transformer or custom vision models) to handle nested and borderless tables.
    *   **Milestone**: Successfully extract the Balance Sheet and P&L into structured JSON.

## Phase 2: The Compliance & Analytics Core (Weeks 3-4)
**Goal**: Implement the "Logic" layer that checks data against regulations.

*   **Task 2.1: The Digital Rulebook**
    *   Codify IndAS and SEBI checklists into a queryable format.
    *   Create the **Compliance Validation Module** to cross-check extracted JSON data against these rules.
*   **Task 2.2: Automated Analytics Module**
    *   Implement financial ratio calculations (Current Ratio, Debt/Equity).
    *   Build the "Auditor vs. Data" cross-reference tool (checking if Auditor qualifications match financial adjustments).
*   **Task 2.3: Preliminary Examination Feeds**
    *   Integrate APIs for news and legal case scraping.

## Phase 3: The Insight Bot & UI Polish (Weeks 5-6)
**Goal**: Build the user-facing interaction layer (The "Wow" Factor).

*   **Task 3.1: NFRA Insight Bot (RAG Implementation)**
    *   Setup Vector Database (e.g., Milvus/Pinecone) for semantic search.
    *   Implement citation-backed responses (Bot must quote the page number).
*   **Task 3.2: Dashboard & Visualization**
    *   Build the Frontend (React/Next.js) for the "Compliance Report Generator".
    *   Implement interactive visualizations for financial trends.

## Phase 4: Optimization & Deployment (Week 7-8)
**Goal**: Performance tuning and preparing for the On-Premises Round.

*   **Task 4.1: Performance Optimization**
    *   Optimize inference time for large PDFs (>500 pages).
*   **Task 4.2: Security Hardening**
    *   Ensure PII redaction and role-based access control (RBAC).
*   **Final Deliverable**: A deployable containerized solution ready for the AIKosh dataset.
