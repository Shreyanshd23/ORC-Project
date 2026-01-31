# 04. FUNCTIONAL SPECIFICATIONS (INCEPTION)

## System Overview
The **AI-FRC Engine** is a deterministic system wrapped in probabilistic intelligence. It does not "guess" compliance; it *verifies* it.

## Key Modules & Workflows

### Module 1: The "Ingestor" (Smart Document Processor)
*   **Input**: PDF (Native or Scanned)
*   **Process**:
    1.  **Format Detection**: Checks if Vector PDF or Raster (Image).
    2.  **Layout Analysis**: Segments page into `Header`, `Footer`, `Body`, `Table`, `Image`.
    3.  **Section Classification**: Assigns a label to every page (e.g., "Page 45 is Balance Sheet").
*   **Output (Artifact)**: `Universal_Document_JSON`
    *   A structured representation of the PDF where tables are preserved as 2D arrays and text is linked to section headers.

### Module 2: The "Digital Auditor" (Compliance Engine)
This is the core differentiator. It uses a **Rule-Based + Semantic Hybrid** approach.

#### Workflow: The "Checklist" Loop
1.  **Load Rulebook**: System loads the `IndAS_Checklist.json`.
    *   *Example Rule*: "IndAS 1, Para 10(b): Complete set of financial statements must comprise a Setup of Profit and Loss."
2.  **Agent Execution**:
    *   *Step A*: Did we find a section labeled "Profit and Loss"? (Y/N)
    *   *Step B (If Yes)*: Does it contain "Profit for the period"? (Semantic Search)
    *   *Step C (Validation)*: Does "Profit for the period" equal "Total Income" minus "Total Expenses"? (Arithmetic Check)
3.  **Flagging**:
    *   If Step C fails: Create `Non-Compliance Flag` (Severity: High).
    *   Citation: "Page 46 (P&L) vs Page 48 (Notes)".

### Module 3: The "Analyst" (Automated Analytics)
*   **Objective**: Convert static numbers into financial health indicators.
*   **Features**:
    *   **Trend Analysis**: Compare Current Year (CY) vs Previous Year (PY).
    *   **Anomaly Detection**: If "Travel Expenses" jumped 500%, Flag it.
    *   **Ratio Calculation**: Current Ratio, Debt-Equity Ratio.

### Module 4: The "Watchdog" (Preliminary Examination)
*   **Objective**: External Signal Correlation.
*   **Process**:
    *   API calls to Google News / Bing Search (simulated for dev).
    *   Keywords: "[Company Name] + Fraud", "[Company Name] + Litigation".
    *   Logic: If News Sentiment is "Negative" AND "Auditor Report" has "Qualified Opinion" -> **Risk Score: Critical**.

---

## Detailed Deliverables List (Pre-Coding)

To mitigate "Government Office" complexity (Ambiguity, Changing Requirements), we need these concretely defined:

### 1. The "Golden Schema"
We must define the standardized JSON output for an Annual Report.
```json
{
  "company_meta": { "cin": "string", "name": "string" },
  "financials": {
    "balance_sheet": {
      "assets": {
        "non_current": [ { "line_item": "Property Plant Equipment", "cy": 100, "py": 90 } ]
      }
    }
  },
  "compliance_report": [
    {
      "rule_id": "IndAS-1-10b",
      "status": "PASS",
      "evidence": "Found on Page 45",
      "confidence": 0.98
    }
  ]
}
```

### 2. The Failure Mode Analysis (FMA)
Government systems fail when they encounter unexpected input. We need a plan for:
*   **Partial Scans**: What if pages 10-12 are missing? -> System must report "Data Missing" not crash.
*   **Bad OCR**: What if "100,000" reads as "100.000"? -> Logic to cross-verify totals (Sum of parts = Total).
*   **Language**: Hindi/English mixed documents.

### 3. User Roles (RBAC)
*   **Uploader**: Can submit documents.
*   **Reviewer**: Can edit the "Parsed Data" (Human-in-the-Loop).
*   **Auditor**: Can view final reports and "Chat" with the bot.
*   **Admin**: System config.
