# 05. PROJECT EXECUTION PLAN (INCEPTION)

## The Reality Check
In a real government implementation:
*   **Data is Dirty**: Scanned PDFs will be tilted, stained, or have handwritten notes.
*   **Regulations are Ambiguous**: IndAS interpretations vary between auditors.
*   **Scope Creep is Real**: "Can you also check GST filings?" (Focus on the prompt first).

To win, we work in **Iterative Circles**, not a waterfall.

---

## Phase 1: The "Robust Eye" (Weeks 1-2)
**Focus**: Can we read the document correctly?
*We do NOT worry about compliance logic here. If we can't read the table, we can't check the math.*

*   **Step 1.1**: Set up the **Local LLM Bench**. Get Llama-3 running on vLLM.
*   **Step 1.2**: Build the **Pipeline V1**. `PDF -> Images -> PaddleOCR -> Raw Text`.
*   **Step 1.3**: The **Structure Mapper**.
    *   Train/Code heuristics to find the "Start" and "End" of the 5 key sections.
    *   *Deliverable*: A visual debugger where we can see a PDF and the system draws bounding boxes around "Balance Sheet" and "Audit Report".

## Phase 2: The "Digital Clerk" (Weeks 3-4)
**Focus**: Can we extract structured data?
*Now that we have the pages, turn them into JSON.*

*   **Step 2.1**: **Table Extraction**. Implement the algorithm to convert "Page 45 Image" into "Pandas DataFrame".
*   **Step 2.2**: **Header Reconciliation**. Map "Total Revenue", "Rev. from Ops", "Income" all to a standardized key `total_revenue`. *This is the hardest part.*
*   **Step 2.3**: **Basic Math Checks**.
    *   Does `Assets` = `Liabilities + Equity`?
    *   If NO, the OCR is wrong or the table structure is misread. **Auto-Correction Loop**.

## Phase 3: The "Junior Auditor" (Weeks 5-6)
**Focus**: Compliance & Cross-Referencing.

*   **Step 3.1**: **The Rules Engine**.
    *   Implement 10 high-impact IndAS rules first. Don't try to do all 500.
    *   Example: "Does the Audit Report mention 'Material Uncertainty'?"
*   **Step 3.2**: **The Insight Bot (RAG)**.
    *   Index the "Notes to Accounts".
    *   Enable queries like: "List all related party transactions."

## Phase 4: The "Dashboards & Polish" (Week 7-8)
**Focus**: UX and Presentation.

*   **Step 4.1**: Build the **Next.js Dashboard**.
    *   "Compliance Scorecard" view.
    *   "Red Flag" Highlighting.
*   **Step 4.2**: **Evidence Viewer**. Click a number -> Jump to the PDF page and highlight the row. **This is the WOW factor.**

---

## Immediate Next Steps (Day 0)
1.  **Initialize Git Repository**.
2.  **Scaffold the Project Structure** (Monorepo: `frontend`, `backend`, `ai-engine`).
3.  **Environment Setup**: Docker, vLLM, PostgreSQL.
4.  **Download Sample Annual Reports** (Tata Steel, Reliance, small cap companies) to test variety.
