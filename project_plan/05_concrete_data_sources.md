# 05. CONCRETE DATA SOURCES & TOOLS (ZERO AMBIGUITY)

## Test Data: Where to Get Annual Reports (FREE)

### Primary Source: BSE India (Bombay Stock Exchange)
**URL**: https://www.bseindia.com/corporates/annualreports.aspx
**Cost**: Free (public disclosure requirement)
**Coverage**: 5000+ listed companies
**Format**: PDF (native and scanned)

#### Specific Companies for Testing
**Large Cap (Complex)**:
- Reliance Industries (CIN: L17110MH1973PLC019786)
- Tata Steel (CIN: L27100MH1907PLC000260)
- HDFC Bank (CIN: L65920MH1994PLC080618)

**Mid Cap (Moderate)**:
- Motherson Sumi (Auto parts)
- Page Industries (Textile)

**Small Cap (Simple)**:
- Any company with market cap under ₹5000 Cr
- Often simpler Balance Sheets, good for initial testing

**PSU (Bilingual - Hindi/English)**:
- BHEL (Bharat Heavy Electricals Limited)
- Coal India Limited
- NTPC Limited
- Source: These often have Hindi sections for government mandate compliance

### Secondary Source: NSE India
**URL**: https://www.nseindia.com/ → Company Search → Annual Reports
**Same coverage as BSE**

### Tertiary Source: MCA Portal (Ministry of Corporate Affairs)
**URL**: https://www.mca.gov.in/content/mca/global/en/mca/master-data/MDS.html
**Coverage**: ALL registered companies (including unlisted)
**Limitation**: Requires registration, slower download

---

## Regulatory Documents: Free & Official

### IndAS Standards
**Source**: ICAI (Institute of Chartered Accountants of India)
**URL**: https://www.icai.org/resources.shtml?mod=1
**Files Needed**:
- IndAS Volume I (PDF, ~800 pages)
- IndAS Volume II (PDF, ~900 pages)
- Conceptual Framework (PDF, ~60 pages)

**Parsing Strategy**:
- Extract all "Para X" sections using regex
- Store as: `{"IndAS_1_Para_10b": "Complete set of financial statements shall comprise..."}`

### Companies Act 2013, Schedule III
**Source**: MCA Portal
**URL**: https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/acts.html
**File**: Schedule III (Format of Balance Sheet)
**Key Section**: Division I (Companies not engaged in financial services)

### SEBI LODR Regulations
**Source**: SEBI Official
**URL**: https://www.sebi.gov.in/legal/regulations/
**File**: LODR 2015 (Latest Amendment)
**Focus**: Regulation 33 (Financial Disclosures)

### RBI Guidelines (For Financial Institutions Only)
**Source**: RBI Official
**URL**: https://www.rbi.org.in/Scripts/NotificationUser.aspx
**Relevant Only**: If processing Bank/NBFC Annual Reports

---

## Tool Versions (Exact)

### OCR & Document Processing
- **PaddleOCR**: Version 2.7.3 (Latest stable as of Jan 2026)
  - License: Apache 2.0
  - Installation: `pip install paddlepaddle==2.6.0 paddleocr==2.7.3`
  - Model: `PP-OCRv4` (English + Hindi)

- **Docling**: Version 1.0.0 (IBM Open Source)
  - License: MIT
  - Installation: `pip install docling==1.0.0`
  - Purpose: Layout analysis, table detection

- **PyMuPDF (Fitz)**: Version 1.24.0
  - License: AGPL
  - Purpose: Native PDF text extraction (fast path)

### LLM & Inference
- **vLLM**: Version 0.6.3
  - License: Apache 2.0
  - Purpose: High-throughput serving
  - Model Support: Llama-3, Mistral

- **Llama-3-70B-Instruct** OR **Mistral-Large-2-123B**
  - Source: Hugging Face (Open Weights)
  - Model ID: `meta-llama/Meta-Llama-3-70B-Instruct`
  - Quantization: GPTQ 4-bit (fits 48GB VRAM)

- **Ollama**: Version 0.5.0 (Optional for dev)
  - License: MIT
  - Purpose: Easy local LLM management

### Vector Database
- **Qdrant**: Version 1.9.0
  - License: Apache 2.0
  - Deployment: Standalone Docker
  - Storage: On-disk (persistent)

### Queue & Workers
- **RabbitMQ**: Version 3.13.0
  - License: MPL 2.0
  - Purpose: Message queue
  - Management UI: Enabled (Port 15672)

- **Celery**: Version 5.4.0
  - License: BSD
  - Purpose: Task queue workers
  - Backend: RabbitMQ

### Database
- **PostgreSQL**: Version 16.2
  - License: PostgreSQL License (OSI Approved)
  - Extensions: `pg_trgm` (fuzzy text search)

### Object Storage
- **MinIO**: Version RELEASE.2024-01-28T22-35-53Z
  - License: AGPL v3
  - Purpose: S3-compatible storage for PDFs
  - Encryption: At-rest enabled

### Frontend
- **Next.js**: Version 14.2.0
  - License: MIT
  - Framework: React 18

- **Shadcn/UI**: Latest (Component library)
  - License: MIT
  - Accessibility: ARIA compliant

---

## Hardware Specifications (Indian Govt Procurement Standards)

### Minimum Viable (Stage 2 Demo)
**Compliant With**: GeM (Government e-Marketplace) Category: High-End Server

**Specs**:
- CPU: Intel Xeon Silver 4314 (16-core) OR AMD EPYC 7313P
- RAM: 64GB DDR4 ECC
- GPU: NVIDIA T4 (16GB VRAM) - GeM Listed
- Storage: 1TB NVMe SSD
- Network: 10Gbps NIC

**Indian Supplier Examples**:
- HCL TechBee Servers
- Wipro Infotech
- Netweb Technologies (Make in India)

**Estimated Cost**: ₹4-5 Lakh (per unit)

### Production Deployment (Stage 3 - On Premises)
**Cluster Setup**:
- 1x Load Balancer Node (No GPU)
- 2x API Server Nodes (No GPU)
- 4x GPU Worker Nodes (Each with 1x NVIDIA T4)
- 1x Database Node (High RAM)
- 1x Storage Node (MinIO - High Disk)

**Total Estimated Cost**: ₹18-22 Lakh (one-time capex)
**Annual Maintenance**: ₹2-3 Lakh (power + AMC)

---

## Embedding Models (Free & Open Source)

### For Vector Search (RAG)
**Model**: `BAAI/bge-m3`
**Source**: Hugging Face
**License**: MIT
**Dimensions**: 1024
**Language Support**: Multilingual (English + Hindi)
**File Size**: 2.2GB
**Purpose**: Semantic search in "Notes to Accounts"

---

## Change Management & Training Plan (Government-Specific)

### Training Modules for NFRA Staff
**Duration**: 2 weeks (phased rollout)

**Module 1: System Overview (2 hours)**
- Who: All NFRA officers (100+ users)
- Format: Video + PDF guide
- Language: English + Hindi subtitles

**Module 2: Document Upload (1 hour)**
- Who: Level 1 Users (Uploaders)
- Hands-on: Practice uploading 5 test reports

**Module 3: Report Review (3 hours)**
- Who: Level 2-3 Users (Analysts, Auditors)
- Focus: Reading compliance flags, using Insight Bot

**Module 4: Admin Panel (2 hours)**
- Who: Level 4 Users (System Admins)
- Focus: User management, system logs

**Support**:
- Help Desk: WhatsApp Business + Email
- SLA: 4-hour response time (business hours)
- Escalation: Direct line to dev team (first 6 months)

---

## MeitY Cloud (MeghRaj) Deployment Specifics

### Compliance Requirements
**Cloud Service Provider**: NIC (National Informatics Centre) OR CDAC
**Data Center Location**: Must be in India (Preferably Delhi/Pune)
**Empanelment**: Solution must be on MeitY's approved vendor list

### Deployment Format
**Containerization**: Docker (not proprietary platforms)
**Orchestration**: Kubernetes 1.28+ (open source)
**Helm Charts**: Provided for easy deployment
**Namespace Isolation**: Separate namespace per environment (dev/staging/prod)

### Network Policy
**Internet Access**: LLM inference pods have ZERO internet
**Inbound**: Only via Nginx Ingress (TLS 1.3)
**Outbound**: Only MinIO (object storage) and PostgreSQL
**Firewall**: Cert-In approved configs

---

## Cert-In Audit Log Requirements (Specific)

### Mandatory Log Fields
**Every log entry must contain**:
- Timestamp (ISO 8601 format, IST timezone)
- User ID (PAN-based or NFRA employee ID)
- Action (e.g., "UPLOAD_REPORT", "OVERRIDE_FLAG")
- Resource (e.g., "Company CIN: L17110MH1973PLC019786")
- Result (SUCCESS / FAILURE)
- IP Address
- Session ID

### Log Retention
**Period**: 90 days (active), 5 years (archived)
**Storage**: Write-only PostgreSQL table
**Export**: Daily backup to encrypted S3 (MinIO)

### Alert Triggers
**Immediate Notification**:
- Failed login attempts (>3 in 5 minutes)
- Data export actions (CSV download of >1000 records)
- Admin user creation
- System configuration changes

**Notification Channel**: Email to designated NFRA security officer

---

## Bilingual Support (Hindi) - Concrete Plan

### OCR Configuration
**PaddleOCR Models**:
- English: `en_PP-OCRv4_server_infer`
- Hindi: `hindi_PP-OCRv3_server_infer`

**Workflow**:
- Detect language per page using `langdetect` library
- Route to appropriate OCR model
- Merge results preserving page structure

### UI Language Toggle
**Frontend**: `next-intl` library (Version 3.10.0)
**Supported**: English, Hindi
**Translation Files**: `en.json`, `hi.json`
**Right-to-Left**: Not needed (Devanagari is left-to-right)

---

## Performance Benchmarking Tools (Free)

### Load Testing
**Tool**: Locust (Version 2.24.0)
**License**: MIT
**Purpose**: Simulate 100 concurrent users
**Metrics**: Response time, throughput, error rate

### Profiling
**Tool**: Py-Spy (Version 0.3.14)
**License**: MIT  
**Purpose**: Find Python bottlenecks
**Usage**: Attach to Celery workers

### Monitoring
**Tool**: Prometheus + Grafana
**Versions**: Prometheus 2.50.0, Grafana 10.4.0
**Dashboards**: Pre-built templates for FastAPI, PostgreSQL, GPU usage

---

## Success Criteria (Measurable & Specific)

### Phase 1 (Week 2 Milestone)
- OCR 10 Annual Reports
- Character Error Rate: <2% (native), <5% (scanned)
- Processing Speed: <10 min per 500-page PDF

### Phase 2 (Week 4 Milestone)
- Extract Balance Sheets from 15 companies
- Field Accuracy: >90% (Total Assets, Total Liabilities)
- Table Structure Preservation: >85%

### Phase 3 (Week 6 Milestone)
- Implement 10 IndAS compliance rules
- True Positive Rate: >75%
- False Positive Rate: <15%

### Final Demo (Week 8)
- End-to-end demo: Upload Reliance 2024 report
- Total Time: <5 minutes
- Compliance report generated with citations
- Insight Bot answers 3 questions correctly
