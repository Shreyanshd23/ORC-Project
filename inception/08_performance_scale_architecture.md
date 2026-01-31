# 07. Performance Benchmarks & Scale Architecture

## The Core Promise: "Fast Enough for Government"

Government systems have a reality that startups often miss: **Uptime > Speed**.
A system that processes 10 reports/hour but never crashes is better than one that does 100/hour but fails every week.

---

## Performance SLA Targets

### Tier 1: Single Document Processing

| Stage | Input | Target Time | Hardware Assumption | Justification |
|:------|:------|:------------|:--------------------|:--------------|
| **OCR (Scanned)** | 500-page scanned PDF | <5 minutes | 8-core CPU, 16GB RAM | PaddleOCR processes ~2 pages/second on CPU. |
| **OCR (Native)** | 500-page native PDF | <30 seconds | Same | Docling skips OCR, direct text extraction. |
| **Table Extraction** | 20 tables (complex) | <2 minutes | 1x NVIDIA T4 GPU (16GB VRAM) | Table Transformer inference: ~5-10 sec/table. |
| **Compliance Check** | Full report (all rules) | <1 minute | CPU (vLLM offloaded) | Rule-based logic + 10 LLM calls. |
| **Total (Scanned)** | 500-page scanned PDF | **<8 minutes** | 8-core CPU, 16GB RAM, 1x T4 GPU | End-to-end from upload to report. |
| **Total (Native)** | 500-page native PDF | **<3.5 minutes** | Same | Optimistic case. |

### Tier 2: Batch Processing (The Real-World Case)

**Scenario**: NFRA receives 1,000 Annual Reports during filing season.

| Metric | Target | Architecture | Justification |
|:-------|:-------|:-------------|:--------------|
| **Throughput** | 200 reports/day | 4-node cluster (8 cores each) | Each node processes 1 report every 8 min = 7.5 reports/hr. 4 nodes × 7.5 × 8 hours = 240 reports/day. |
| **Queue Wait Time** | <30 minutes | RabbitMQ + Celery | Jobs are queued and picked by available workers. |
| **Failure Rate** | <1% | Retry logic (max 3 attempts) | Infrastructure transient errors. |
| **Peak Load Handling** | 100 simultaneous uploads | MinIO (Object Storage) | Uploads are cheap (just file write). Processing starts async. |

---

## Scale Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                    │
│                     (Distributes Requests)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴────────────────┐
        │                                │
┌───────▼────────┐              ┌────────▼───────┐
│  Frontend      │              │  API Server    │
│  (Next.js)     │◄─────────────┤  (FastAPI)     │
│  Port: 3000    │   REST API   │  Port: 8000    │
└────────────────┘              └────────┬───────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                 ┌───────▼──────┐ ┌──────▼─────┐ ┌──────▼─────┐
                 │ PostgreSQL   │ │ RabbitMQ   │ │  MinIO     │
                 │ (Metadata)   │ │ (Queue)    │ │ (PDFs)     │
                 └──────────────┘ └──────┬─────┘ └────────────┘
                                         │
                                 ┌───────┴───────┐
                                 │  Celery       │
                                 │  Workers      │
                                 │  (4 nodes)    │
                                 └───────┬───────┘
                                         │
                        ┌────────────────┼────────────────┐
                        │                │                │
                ┌───────▼──────┐ ┌───────▼──────┐ ┌──────▼─────┐
                │  GPU Worker  │ │  GPU Worker  │ │ GPU Worker │
                │  (OCR +      │ │  (OCR +      │ │ (OCR +     │
                │   Tables)    │ │   Tables)    │ │  Tables)   │
                └──────┬───────┘ └──────┬───────┘ └──────┬─────┘
                       │                │                │
                       └────────────────┼────────────────┘
                                        │
                                ┌───────▼───────┐
                                │   Qdrant      │
                                │  (Vector DB)  │
                                │  (For RAG)    │
                                └───────────────┘
```

### Key Components Explained

1. **Load Balancer (Nginx)**: 
   - Handles HTTPS termination.
   - Routes traffic to API servers.

2. **API Server (FastAPI)**:
   - Lightweight. Handles upload, metadata CRUD.
   - Does NOT do heavy computation (offloads to Celery).

3. **RabbitMQ + Celery**:
   - **Queue**: RabbitMQ stores pending jobs.
   - **Workers**: 4 Celery worker nodes pick jobs and process PDFs.
   - **Why**: Decouples upload (fast) from processing (slow).

4. **GPU Workers**:
   - Dedicated machines with NVIDIA T4 GPUs.
   - Run PaddleOCR and Table Transformer.
   - **Scaling**: Add more GPU nodes during peak season.

5. **Qdrant (Vector DB)**:
   - Stores embeddings for the "Insight Bot".
   - Supports hybrid search (keyword + semantic).

---

## Hardware Requirements

### Minimum Viable Deployment (MVP)
**For Stage 2 Demo (10 reports)**:
- **Server**: 1x 16-core CPU, 64GB RAM, 1x NVIDIA T4 GPU (16GB VRAM)
- **Storage**: 500GB SSD
- **Cost**: ~₹2-3 Lakh (AWS/GCP equivalent, or on-prem server)

### Production Deployment (1000s of reports)
**For NFRA Full Rollout**:
- **API Servers**: 2x 8-core CPU, 32GB RAM (redundancy)
- **GPU Workers**: 4x 16-core CPU, 64GB RAM, 1x T4 GPU each
- **Database**: 1x 8-core CPU, 64GB RAM (PostgreSQL + Qdrant)
- **Storage**: 10TB HDD (MinIO for PDFs)
- **Cost**: ~₹15-20 Lakh (one-time capex) + ₹1-2 Lakh/year (power/maintenance)

---

## Performance Optimization Strategies

### 1. **Lazy OCR**
**Problem**: OCR is expensive. We don't need to OCR every page.
**Solution**: 
- Only OCR pages flagged as "Table" or "Audit Report" by the Structure Mapper.
- Skip headers/footers (they're repetitive).

**Impact**: 40% reduction in OCR time.

### 2. **Parallel Table Processing**
**Problem**: A report has 50 tables. Processing them sequentially takes 8 minutes.
**Solution**:
- Use `concurrent.futures` to process 4 tables simultaneously (if 1 GPU with 16GB VRAM).

**Impact**: 4x speedup (8 min → 2 min).

### 3. **Caching Layer**
**Problem**: Same company submits reports every year. Some sections (like "Company Info") are identical.
**Solution**:
- Hash the "Company Info" page.
- If hash matches last year's, reuse the extracted data.

**Impact**: 10-15% time saving on repeat filings.

### 4. **Progressive Reporting**
**Problem**: User waits 8 minutes with no feedback.
**Solution**:
- WebSocket-based progress updates.
  - "20% - OCR Complete"
  - "50% - Tables Extracted"
  - "80% - Compliance Check Running"

**Impact**: Better UX (user doesn't think the system is frozen).

---

## India-Specific Performance Considerations

### 1. **Power Outages**
**Problem**: Government data centers in Tier 2 cities may have unstable power.
**Solution**:
- Celery workers auto-resume jobs after restart.
- PostgreSQL Write-Ahead Logging (WAL) ensures no data loss.

### 2. **Low Bandwidth**
**Problem**: NFRA officers in regional offices uploading 50MB PDFs on 2 Mbps connections.
**Solution**:
- Chunked uploads (resume if connection drops).
- Compression (PDFs are often bloated; we can compress to 70% size without quality loss).

### 3. **Hindi OCR Latency**
**Problem**: PaddleOCR is slower on Devanagari (complex character shapes).
**Solution**:
- Pre-process: Detect language per page. Use separate models (English-only vs Hindi-only).

---

## Monitoring & Observability

We instrument the system to detect performance degradation early.

### Key Metrics to Track

| Metric | Tool | Alert Threshold | Action |
|:-------|:-----|:----------------|:-------|
| **Queue Depth** | RabbitMQ Dashboard | >100 jobs | Add more Celery workers |
| **GPU Utilization** | `nvidia-smi` | <50% | Check for bottlenecks elsewhere |
| **API Response Time** | Prometheus + Grafana | 95th %ile >2 sec | Scale API servers |
| **Database Connections** | PostgreSQL logs | >80% capacity | Add connection pooling |

---

## The "8-Week vs Production" Trade-off

### For Stage 2 (Virtual Challenge Round)
**Reality**: We have 1 server, processing 10 test reports.
**What we SKIP**:
- Multi-node cluster (Use 1 server)
- Load balancer (Direct FastAPI)
- Advanced caching (Process everything fresh)

**What we DEMO**:
- End-to-end processing of 1 complex report in <8 minutes.
- Progress bar showing real-time status.

### For Stage 3 (On-Premises Round)
**Reality**: We demonstrate production-readiness.
**What we ADD**:
- Kubernetes deployment (show scalability)
- Load testing results (100 concurrent users)
- Disaster recovery plan (backup/restore demo)

---

## Honest Performance Expectations

| Metric | Optimistic | Realistic | Pessimistic |
|:-------|:-----------|:----------|:------------|
| **Processing Time (Native PDF)** | 2 min | 3.5 min | 5 min (if complex tables) |
| **Processing Time (Scanned)** | 5 min | 8 min | 12 min (poor scan quality) |
| **Throughput (Single Server)** | 10 reports/hr | 7 reports/hr | 5 reports/hr |
| **Throughput (4-Node Cluster)** | 40 reports/hr | 28 reports/hr | 20 reports/hr |

**Key Insight**: We promise **8 min/report** and deliver it 90% of the time. The 10% outliers (900-page reports, terrible scans) we flag for manual review.

---

## Success Criteria

1. **Speed**: Process Reliance 2024 Annual Report (500 pages, native PDF) in <4 minutes.
2. **Scale**: Handle 100 simultaneous uploads without crash.
3. **Reliability**: 99% success rate on test corpus (20 reports).
