# 06. DATA SECURITY & GOVERNANCE (GOVERNMENT-READY)

## The Sensitivity Context
We are dealing with the internal functioning of the **National Financial Reporting Authority (NFRA)**.
*   **Documents**: Annual Reports (Public) + potentially Draft Audit Reports (Confidential).
*   **Data**: Director PANs, Signatures, Internal Remarks.
*   **Constraint**: "Sovereign AI" - Data must reside within India/MeitY Cloud.

## Security Architecture

### 1. Data Processing Isolation (The "Air Gap" Strategy)
*   **Network Policy**: The Inference Engine (Code running the LLM) has **NO Internet Access**.
*   **Update Mechanism**: Models are pre-downloaded. Updates are applied via manual container refreshes, not run-time downloads.

### 2. PII Redaction Pipeline
Before any text chunk is indexed into the Vector Database (Qdrant):
*   **Step 1**: Run `Presidio` (Microsoft) or `Spacy` NER model.
*   **Step 2**: Identify Entities: `PHONE_NUMBER`, `EMAIL_ADDRESS`, `OAD_UID` (Aadhaar), `PAN`.
*   **Step 3**: Redact/Tokenize.
    *   Original: "Director PAN: ABCDE1234F"
    *   Indexed: "Director PAN: <REDACTED>"
*   **Why**: Even if the vector database is compromised, personal identifiers are safe.

### 3. Role-Based Access Control (RBAC)
We utilize **Keycloak** or **Django Native Auth** for granular permissions.
*   **Level 1 (Public)**: View extracted Metadata (Company Name, Year).
*   **Level 2 (Analyst)**: View Flagged Risks and Compliance Scores.
*   **Level 3 (Auditor)**: Access to Source Documents and Evidence Snippets.
*   **Level 4 (Admin)**: System Logs and User Management.

### 4. Audit Trails (The "Watcher")
In a government setup, "Who checked this?" is as important as the check itself.
*   **Immutable Logs**: Every action is logged to a write-only table.
    *   `[2026-01-31 10:00:00] User: Officer_Sharma | Action: Override_Risk_Flag | Reason: "Typos in original doc"`
*   **AI Explainability**: The "Insight Bot" must cite sources.
    *   Bad: "The revenue is 500 Cr."
    *   Good: "The revenue is 500 Cr, based on the Table 'Statement of P&L' on Page 45, Row 3."

## Deployment Strategy (MeghRaj / MeitY Cloud Compatible)
*   **Containerization**: Docker Compose / Kubernetes (Helm Charts).
*   **Storage**: MinIO (S3 Compatible Object Storage) for PDFs. Self-hosted.
*   **Encryption**:
    *   At Rest: AES-256 for PostgreSQL and MinIO.
    *   In Transit: TLS 1.3 for all internal API calls.

## Compliance Standards
This architecture ensures we meet:
1.  **Digital Personal Data Protection (DPDP) Act, 2023**.
2.  **MeitY Guidelines** for Government Data Classification.
3.  **Cert-In** Security Auditing standards.

---

**Related Documents**:
- [04_tech_stack_architecture.md](04_tech_stack_architecture.md) - Sovereign FOSS choices
- [05_concrete_data_sources.md](05_concrete_data_sources.md) - Exact tool versions & audit log formats
- [07_performance_benchmarks.md](07_performance_benchmarks.md) - Disaster recovery SLAs
