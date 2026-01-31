# 03. TECHNICAL ARCHITECTURE & FEATURE SCALABILITY (INCEPTION)

## Core Philosophy: "Index Everything, Extract One"
To meet the challenge's stringent requirements for "Automated Analytics" and "ESG" compliance, we cannot simply extract tables from the Balance Sheet. We must understand the document as a whole.

### The Problem with Simple Extraction
A traditional parser looking only for "Total Assets" might find it in:
1.  The Consolidated Balance Sheet (Correct)
2.  The Standalone Balance Sheet (Sometimes needed)
3.  A random table in the "Management Discussion" (Incorrect)

### The Solution: Semantic Structure Mapping
Our system first builds a **Semantic Map** of the document before extracting a single number. This ensures context-aware extraction.

#### 1. The Mapper Logic
The `mapper.py` module identifies page ranges for specific "Zones of Interest". This future-proofs the application for Phases 2 and 3.

| Section | Keywords (Heuristics) | Critical Use Case |
| :--- | :--- | :--- |
| **A. Corporate Identity** | "Corporate Information", "CIN" | Entity Resolution (Who are we auditing?) |
| **B. Auditor's Verdict** | "Independent Auditor's Report", "Qualified Opinion" | **Risk Assessment**: Detects if the human auditor flagged fraud. |
| **C. Financial Statements** | "Balance Sheet", "Profit and Loss", "Cash Flow" | **Quantitative Analysis**: Core data for ratios and IndAS checks. |
| **D. Governance** | "Corporate Governance", "Board of Directors" | **Entity Checks**: Verifying board composition against Companies Act. |
| **E. ESG / BRSR** | "Business Responsibility", "Principle 1" | **Sustainability**: For SEBI ESG Framework compliance. |

#### 2. Data Structure Design
The output of the mapping stage is a JSON object that guides the subsequent extraction agents.

```json
{
  "metadata": {
    "company_name": "Tata Steel",
    "financial_year": "2024-25",
    "document_id": "UUID-1234"
  },
  "semantic_map": {
    "auditors_report": { "start_page": 34, "end_page": 42, "status": "qualified" },
    "financial_statements": { 
        "balance_sheet": { "page": 45, "type": "consolidated" },
        "pnl": { "page": 46 },
        "cash_flow": { "page": 47 },
        "notes_to_accounts": { "range": [50, 95] }
    },
    "brsr_report": { "start_page": 12, "end_page": 30 },
    "corporate_governance_report": { "start_page": 96, "end_page": 110 }
  }
}
```

## Citations & Regulatory Frameworks
The solution is strictly architected to validate against the following benchmarks:

### 1. Financial Reporting Standards
*   **Indian Accounting Standards (IndAS)**:
    *   *Source*: [ICAI IndAS Vol 1 & 2](https://www.icai.org/resources.shtml?mod=1)
    *   *Usage*: Validating format and disclosures of Financial Statements.
*   **General Instructions for Financial Statements**:
    *   *Source*: [Schedule III, Companies Act 2013](https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/acts.html?act=NTk2MQ==)
    *   *Usage*: Checking the hierarchy of line items (e.g., Equity -> Liabilities).

### 2. Disclosures & Governance
*   **SEBI LODR (Listing Obligations and Disclosure Requirements)**:
    *   *Source*: [SEBI Regulations 2015](https://www.sebi.gov.in/)
    *   *Usage*: Verifying timely disclosures and board composition.
*   **RBI Disclosure Norms**:
    *   *Source*: [RBI Notifications](https://www.rbi.org.in/)
    *   *Usage*: Specific checks for Financial Institutions/NBFCs.

### 3. Sustainability (ESG)
*   **BRSR Core Framework**:
    *   *Source*: [SEBI ESG Disclosures](https://www.sebi.gov.in/legal/circulars/jul-2023/brsr-core-framework-for-assurance-and-esg-disclosures-for-value-chain_73854.html)
    *   *Usage*: Extracting non-financial data points for the "Insight Bot".

## Technical Scalability
*   **Chunking Strategy**: Documents are not fed to the LLM in one go. They are chunked by the *Semantic Map*. The "Auditor's Report" is processed by a specialized `AuditAnalyzer` agent, while the "Balance Sheet" is processed by a `TableExtractor` agent.
*   **Vector Search**: We index the "Notes to Accounts" separately to allow the Insight Bot to answer questions like "Why did the 'Other Expenses' increase?" by retrieving the specific note.
