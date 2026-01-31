# 08. REAL-WORLD VALIDATION PLAN (EXECUTION READY)

## Phase 1: Data Collection (Week 0 - Before Coding)

### Test Corpus Assembly

**Total Reports Needed**: 25

**Category A: Large Cap (10 reports)**
**Source**: BSE India
**Companies**:
- Reliance Industries (FY 2023-24)
- Tata Steel (FY 2023-24)
- HDFC Bank (FY 2023-24)
- Infosys (FY 2023-24)
- ITC Limited (FY 2023-24)
- Larsen & Toubro (FY 2023-24)
- Asian Paints (FY 2023-24)
- Mahindra & Mahindra (FY 2023-24)
- Sun Pharma (FY 2023-24)
- Bharti Airtel (FY 2023-24)

**Characteristics**: 400-600 pages, complex tables, consolidated + standalone financials

**Category B: PSU Bilingual (5 reports)**
**Source**: Company websites
**Companies**:
- BHEL (Hindi sections in Corporate Governance)
- Coal India Limited
- NTPC Limited
- ONGC
- Indian Oil Corporation

**Characteristics**: English + Hindi text, government-specific disclosures

**Category C: Small Cap (5 reports)**
**Source**: BSE India (Market Cap < ₹5000 Cr)
**Purpose**: Simple Balance Sheets for baseline testing

**Category D: Historical Scanned (5 reports)**
**Source**: MCA DCA Portal OR Old BSE archives (1990s-2000s)
**Purpose**: Test OCR on poor quality scans

**Download Method**: Manual download from BSE → Save to project folder

---

## Phase 2: Ground Truth Creation

### Manual Extraction Task

**For Each of 10 Large Cap Reports**:

**Task A: Balance Sheet Extraction**
- Open PDF manually
- Navigate to Consolidated Balance Sheet page
- Extract to Excel:
  - Column headers: "Particulars", "March 31, 2024", "March 31, 2023"
  - All line items: Assets, Liabilities, Equity
  - Totals: Total Assets, Total Liabilities
  - Nested items: Property Plant Equipment → Land, Buildings, etc.

**Task B: Section Mapping**
- Note page numbers:
  - Independent Auditor's Report: Page X to Y
  - Balance Sheet: Page Z
  - Profit & Loss: Page W
  - Cash Flow: Page V
  - Notes to Accounts: Page A to B
  - BRSR (if exists): Page C to D

**Deliverable**: Excel file per company
**Filename**: `ground_truth_reliance_2024.xlsx`
**Sheets**: "Balance_Sheet", "Section_Map"

**Time Estimate**: 2 hours per report
**Total Effort**: 20 hours (2.5 days)

---

## Phase 3: Validation Tests (Week 2, 4, 6 Milestones)

### Test 1: OCR Accuracy (Week 2)

**Objective**: Measure Character Error Rate

**Method**:
- Select 10 random pages from Reliance 2024 report
- Manually type 100 lines of text (ground truth)
- Run PaddleOCR on same pages
- Compare character-by-character

**Metric**: CER = Errors / Total Characters
**Target**: CER < 2% (native PDF)

**Tool**: Python script using Levenshtein distance
**Output**: CSV with per-page CER

---

### Test 2: Table Extraction Accuracy (Week 4)

**Objective**: Measure field-level match rate

**Method**:
- Extract Balance Sheet from all 10 Large Cap reports
- Compare each cell against ground truth Excel
- Count matches vs total cells

**Metrics**:
- Field Accuracy: Exact match (₹5,00,000 Cr)
- Tolerance: ±0.1% allowed for rounding
- Structure Accuracy: Did we maintain parent-child rows?

**Target**: Field Accuracy >95%, Structure >90%

**Output**: Report showing:
- Company: Reliance
- Total Fields: 350
- Matched: 335
- Accuracy: 95.7%

---

### Test 3: Section Detection (Week 2)

**Objective**: Prove Structure Mapper works

**Method**:
- Process all 25 reports
- Compare detected page numbers vs ground truth

**Metric**: Exact page match percentage
**Target**: 100% (deterministic task)

**Output**: JSON comparison file

---

### Test 4: Compliance Rule Testing (Week 6)

**Objective**: Detect non-compliance

**Rules to Test** (10 only):

**Rule 1**: IndAS 1 - Balance Sheet must have Assets = Liabilities + Equity
- Method: Arithmetic check on extracted totals
- Target: 100% correct (math is absolute)

**Rule 2**: IndAS 1, Para 114 - Comparative information required
- Method: Check if "Previous Year" column exists
- Target: 100% (all reports should have CY vs PY)

**Rule 3**: IndAS 24 - Related Party Transactions disclosure
- Method: Search for "Related Party" in Notes to Accounts
- Target: Detect presence in 100% of Large Cap reports

**Rule 4**: IndAS 37 - Contingent Liabilities disclosure
- Method: Search for "Contingent Liabilities" section
- Target: Detect presence (reporting if missing)

**Rule 5**: Schedule III Format - Assets listed before Liabilities
- Method: Check section order in Balance Sheet
- Target: 100% (regulatory format)

**Remaining 5 Rules**: Similar keyword + semantic search logic

**Test Dataset**:
- 10 Large Cap reports (assume compliant)
- Create 2 synthetic "violation" reports (manually edit PDFs to remove sections)

**Metrics**:
- True Positive: Did we flag the 2 violations? (Target: 100%)
- False Positive: Did we incorrectly flag compliant reports? (Target: <10%)

---

## Phase 4: Load Testing (Week 8)

### Test Setup

**Tool**: Locust (Python load testing framework)
**Scenario**: 100 users uploading 50MB PDFs simultaneously

**Infrastructure**: Single GPU server (HCL TechBee setup)

**Test Script**:
- User uploads PDF
- Wait for processing (async)
- Poll status every 5 seconds
- Download final report

**Duration**: 30 minutes

**Metrics to Track**:
- Request throughput: Uploads/second
- Average response time: Time from upload to report ready
- 95th percentile latency: Worst-case wait time
- Error rate: Failed uploads

**Target**:
- Uploads handled: 100/100 (zero drops)
- Avg response: <10 minutes
- 95th percentile: <20 minutes
- Error rate: <1%

---

## Phase 5: User Acceptance Testing (Week 7)

### UAT Participants

**Simulated NFRA Officers**: 5 volunteers (testers or team members roleplaying)

**Roles**:
- 2x Uploaders (Level 1)
- 2x Analysts (Level 2)
- 1x Admin (Level 4)

### UAT Scenarios

**Scenario 1: Upload and Review**
**User**: Uploader
**Task**:
- Login to system
- Upload Reliance 2024 Annual Report
- Wait for processing
- View completion notification

**Success Criteria**:
- Task completed without help: Yes/No
- Time taken: <3 minutes
- Satisfaction: Rate 1-5

**Scenario 2: Compliance Review**
**User**: Analyst
**Task**:
- Open Reliance compliance report
- Identify top 3 flagged risks
- Click on a flag to see evidence

**Success Criteria**:
- Understood the flags: Yes/No
- Found evidence easily: Yes/No
- Satisfaction: Rate 1-5

**Scenario 3: Insight Bot Query**
**User**: Analyst
**Task**:
- Ask: "What is the total revenue?"
- Ask: "List all related party transactions"
- Verify answers against the PDF

**Success Criteria**:
- Bot understood the question: Yes/No
- Answer was correct: Yes/No
- Citation was helpful: Yes/No

**UAT Report**:
- Task completion rate: Target 100%
- Average satisfaction: Target >4/5
- Issues found: Document and prioritize

---

## Phase 6: Demo Preparation (Week 8)

### Demo Script for Judges

**Duration**: 15 minutes

**Minute 0-2: Introduction**
- Problem statement recap
- Our solution overview

**Minute 2-8: Live Demo**

**Scene 1 (3 min): The Upload**
- Open browser to AI-FRC dashboard
- Click "Upload Annual Report"
- Select Reliance 2024 PDF (528 pages)
- Show progress bar (20%... 50%... 80%... Done)
- Time: 6 minutes (pre-processed for speed, show timer)

**Scene 2 (2 min): The Compliance Report**
- Navigate to "Compliance Dashboard"
- Show RED flag: "IndAS 37 - Contingent Liabilities"
- Click flag → Evidence panel shows:
  - "Expected: Contingent Liabilities Note"
  - "Found: Missing"
  - "Recommendation: Manual review required"

**Scene 3 (3 min): The Insight Bot**
- Open chat interface
- Type: "What is the total related party transaction amount for FY2024?"
- Bot responds in 5 seconds:
  - "₹12,500 Cr (Source: Note 42, Page 87)"
- Click citation → PDF viewer opens at Page 87, row highlighted

**Minute 8-12: Technical Deep Dive**
- Show system architecture diagram
- Explain 100% open source stack
- Demonstrate air-gapped deployment (no internet LED indicator)

**Minute 12-15: Q&A**
- Prepare answers for:
  - "How do you handle Hindi text?"
  - "What if the table is wrong?"
  - "Can you scale to 10,000 reports?"

---

## Validation Checklist (Pre-Submission)

### Technical Validation
- [ ] OCR tested on 20 reports, CER < 2%
- [ ] Table extraction tested on 15 companies, accuracy >95%
- [ ] Section detection: 100% page match
- [ ] 10 compliance rules implemented and tested

### Performance Validation
- [ ] Single report processing: <8 minutes (tested 10 times)
- [ ] Load test: 100 concurrent uploads handled
- [ ] System uptime: 99%+ during 1-week test period

### Security Validation
- [ ] PII redaction tested (sample Director PAN redacted)
- [ ] Audit logs verified (every action logged)
- [ ] Air-gap tested (LLM pod has no internet)

### User Validation
- [ ] 5 UAT participants tested
- [ ] Satisfaction score: >4/5
- [ ] Training materials created (English + Hindi)

### Documentation Validation
- [ ] All source code documented
- [ ] Deployment guide written
- [ ] Architecture diagram finalized

---

## Risk Mitigation (Realistic)

### Risk 1: Table Extraction Fails on Complex Nested Tables
**Probability**: Medium (30%)
**Impact**: High (cannot proceed to compliance check)

**Mitigation**:
- Implement confidence scoring (0-1 scale)
- If confidence <0.7, flag for human review
- Provide side-by-side UI (Original PDF vs Extracted Table)
- Human can correct and re-submit

**Fallback**: Process 80% automatically, 20% with human-in-loop

---

### Risk 2: IndAS Rules Are Too Ambiguous
**Probability**: High (50%)
**Impact**: Medium (affects compliance accuracy)

**Mitigation**:
- Focus on 10 OBJECTIVE rules first
- Mark subjective rules as "Requires Manual Interpretation"
- Provide rule explanation in the report (cite IndAS para)

**Fallback**: Position as "First Pass Screening" not "Final Verdict"

---

### Risk 3: Infrastructure Fails During Demo
**Probability**: Low (10%)
**Impact**: Critical (demo failure)

**Mitigation**:
- Pre-process 3 demo reports (Reliance, Tata, BHEL)
- Cache results (show replay if live fails)
- Backup laptop with Docker Compose setup
- Video recording of successful run as fallback

**Fallback**: Show pre-recorded video, explain issue transparently

---

## Success Definition (Final)

### Minimum Viable Success (Stage 2 - Virtual Round)
- Process 5 reports correctly
- 1 live demo successful
- Accuracy >90%
- Shortlisted for Stage 3

### Target Success (Stage 3 - On Premises)
- Process 20 reports in judges' presence
- Accuracy >95%
- Load test passed
- Win the contract

### Moonshot Success
- Process 100 reports
- Accuracy >98%
- Sub-5 minute processing time
- Win + additional features contract
---

**Related Documents**:
- [05_concrete_data_sources.md](05_concrete_data_sources.md) - BSE India URLs & tool versions
- [07_performance_benchmarks.md](07_performance_benchmarks.md) - SLAs & hardware sizing
- [02_index_critical_summary.md](02_index_critical_summary.md) - Overall readiness & confidence scores
