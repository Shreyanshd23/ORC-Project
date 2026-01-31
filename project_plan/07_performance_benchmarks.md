# 07. PERFORMANCE BENCHMARKS (INDUSTRY STANDARD)

## Baseline Performance Targets

### Single Document Processing (SLA)

**Test Document**: Reliance Industries Annual Report 2023-24
**Size**: 528 pages, 45MB PDF (native)
**Hardware**: 16-core CPU, 64GB RAM, 1x NVIDIA T4

**Stage-wise Breakdown**:
- Document Upload & Validation: 5 seconds
- PDF-to-Image Conversion: 45 seconds
- Layout Analysis: 90 seconds
- OCR (Native PDF - fast path): 30 seconds
- Table Extraction (23 tables): 120 seconds
- Compliance Engine: 60 seconds
- Report Generation: 15 seconds
**Total**: 365 seconds (6 minutes)

**Scanned Document** (500 pages, poor quality):
- OCR adds 4 additional minutes
**Total**: 10 minutes

### Batch Processing (Production Scale)

**Scenario**: Annual filing season (March-April)
**Volume**: 500 reports per day
**Operating Hours**: 16 hours (8 AM to 12 AM)

**Single Server Capacity**:
- Reports per hour: 6 (10 min avg)
- Daily capacity: 96 reports (16 hours)

**4-Node GPU Cluster**:
- Combined capacity: 384 reports/day
- Queue buffer: 25% headroom
**Realistic throughput**: 300 reports/day

### Concurrency Test

**Load**: 100 simultaneous PDF uploads
**Expected Behavior**:
- Uploads complete instantly (MinIO handles)
- Processing queued in RabbitMQ
- First 4 start immediately (4 GPU workers)
- Remaining 96 wait in queue
- Average wait time: 8 minutes
- 95th percentile wait time: 35 minutes
- Zero failures

---

## Industry Benchmark Comparison

### Vs Commercial Solutions

**AWS Textract** (Proprietary):
- Cost: $1.50 per 1000 pages
- Speed: 3-5 minutes per 500-page PDF
- Accuracy: ~95% (tables)

**Our Solution**:
- Cost: ₹0 per report (post-infra)
- Speed: 6 minutes per 500-page PDF (comparable)
- Accuracy: Target >95% (same)

**Advantage**: Zero marginal cost, data never leaves premise

### Vs Manual Processing

**Current NFRA Workflow** (Assumed):
- Human analyst manually reviews Annual Report
- Time: 4-6 hours per report
- Coverage: 50-100 reports per quarter

**Our Solution**:
- Automated first-pass: 6 minutes
- Human review (flagged items only): 30 minutes
**Total**: 36 minutes per report
**Speed-up**: 10x faster

---

## Hardware Sizing (GeM Compliant)

### Tier 1: MVP (Stage 2 Demo)
**Use Case**: Process 10 test reports for judges

**Configuration**:
- 1x Server (HCL TechBee HSW130W)
  - CPU: Intel Xeon Silver 4314 (16 cores)
  - RAM: 64GB DDR4 ECC
  - GPU: NVIDIA T4 (16GB)
  - Storage: 1TB NVMe
  - Network: 10Gbps

**GeM Category**: High-Performance Server
**Vendor**: HCL / Netweb / Wipro
**Price**: ₹4.8 Lakh
**Throughput**: 90 reports/day (16-hour operation)

### Tier 2: Production (NFRA Deployment)

**Node Types**:

**A. Load Balancer (1 unit)**:
- CPU: 8 cores
- RAM: 16GB
- No GPU
- Price: ₹1.2 Lakh

**B. API Servers (2 units for redundancy)**:
- CPU: 8 cores each
- RAM: 32GB each
- No GPU
- Price: ₹1.8 Lakh each

**C. GPU Workers (4 units)**:
- CPU: 16 cores each
- RAM: 64GB each
- GPU: 1x T4 each
- Price: ₹4.8 Lakh each

**D. Database Server (1 unit)**:
- CPU: 16 cores
- RAM: 128GB
- NVMe: 2TB
- Price: ₹6.5 Lakh

**E. Storage Server (1 unit - MinIO)**:
- CPU: 8 cores
- RAM: 32GB
- HDD: 20TB (RAID 6)
- Price: ₹3.5 Lakh

**Total Capex**: ₹28.4 Lakh
**Annual Opex**: ₹2.8 Lakh (power + AMC)

**Throughput**: 300 reports/day

---

## Scalability Metrics

### Horizontal Scaling (Add More GPU Workers)

**Baseline**: 4 GPU workers = 300 reports/day

**Scaling**:
- 8 GPU workers = 600 reports/day
- 16 GPU workers = 1200 reports/day

**Bottleneck Check**:
- Database: PostgreSQL 16 can handle 10,000 concurrent connections
- Queue: RabbitMQ can handle 50,000 messages/second
- Storage: MinIO scales linearly with disk addition

**Limit**: GPU worker count (can scale to 100+ if needed)

### Vertical Scaling (Upgrade Hardware)

**Current**: NVIDIA T4 (16GB VRAM)
**Upgrade**: NVIDIA A10 (24GB VRAM)
**Benefit**: Process 2 tables simultaneously instead of 1
**Speed-up**: 30% faster table extraction

---

## Performance Monitoring (Real-Time)

### Key Performance Indicators (KPIs)

**System Health**:
- CPU Usage: <70% sustained
- GPU Usage: 80-90% (optimal utilization)
- RAM Usage: <80%
- Disk I/O: <60% utilization

**Application Metrics**:
- Queue Depth: <50 jobs (healthy)
- Average Processing Time: <8 minutes
- Error Rate: <1%
- API Response Time: <200ms (95th percentile)

### Alerting Thresholds

**Critical Alerts** (Immediate Action):
- GPU worker crash
- Database connection pool exhausted
- Disk usage >90%

**Warning Alerts** (Monitor):
- Queue depth >100
- Processing time >12 minutes (anomaly)
- API latency >500ms

**Monitoring Stack**:
- Prometheus: Metrics collection
- Grafana: Visualization dashboards
- Alertmanager: Email/SMS notifications

---

## Disaster Recovery (Govt Mandate)

### Backup Strategy

**Database Backups**:
- Frequency: Every 6 hours (automated)
- Retention: 30 days active, 1 year archived
- Storage: Encrypted S3 (MinIO on separate node)

**PDF Storage (MinIO)**:
- Replication: 3 copies (RAID 6)
- Backup: Daily incremental
- Retention: Permanent (regulatory requirement)

**Application State**:
- Docker images: Versioned in private registry
- Configuration: Git repository (encrypted secrets)

### Recovery Time Objective (RTO)

**Scenario**: Primary GPU worker fails
- Detection: 2 minutes (health check)
- Action: Kubernetes auto-restart
- Recovery: 5 minutes
**Total RTO**: 7 minutes

**Scenario**: Database corruption
- Detection: Immediate (transaction logs)
- Action: Restore from latest backup
- Recovery: 30 minutes
**Total RTO**: 35 minutes

### Business Continuity

**NFRA Requirement**: System must handle Delhi NCR power outage
**Solution**:
- UPS: 30 minutes battery backup
- Generator: Auto-start on mains failure
- Graceful shutdown: Celery workers finish current job, then halt

---

## Network Performance (India-Specific)

### Upload Speed Requirements

**Assumption**: NFRA officer in Tier 2 city with 10 Mbps connection
**Upload Time** for 45MB PDF:
- Theoretical: 36 seconds
- Realistic (70% efficiency): 52 seconds

**Solution**: Chunked upload with resume capability
**Library**: Uppy.js (resumable uploads)

### On-Premise Network

**Bandwidth**:
- Internal: 10Gbps fiber (between nodes)
- Internet Gateway: 1Gbps (for external searches)

**Latency**:
- API to Database: <1ms (same datacenter)
- API to GPU Worker: <2ms
- User to API: <50ms (within India)

---

## Energy Efficiency (Green IT)

### Power Consumption

**Single Server** (16-core CPU + T4 GPU):
- Idle: 150W
- Load: 400W
- Annual Energy: 3504 kWh (24/7 operation)

**Cost** (Delhi electricity rate ₹8/kWh):
- Annual: ₹28,032 per server

**4-Node Cluster**:
- Total Power: 1600W under load
- Annual Energy: 14,016 kWh
- Annual Cost: ₹1.12 Lakh

**Optimization**:
- Schedule workers to scale down during off-peak hours (12 AM - 6 AM)
- Save 25% energy = ₹28,000/year

---

## Quality of Service (QoS) Tiers

### Tier 1: Express Processing
**SLA**: <5 minutes (native PDF)
**Use Case**: Urgent NFRA investigation
**Cost Model**: Priority queue (jump ahead)

### Tier 2: Standard Processing
**SLA**: <10 minutes (native), <15 minutes (scanned)
**Use Case**: Regular filings
**Cost Model**: Default queue

### Tier 3: Batch Processing
**SLA**: 24-hour turnaround
**Use Case**: Historical analysis (1000+ old reports)
**Cost Model**: Lowest priority, off-peak processing

---

## Compliance SLA (India-Specific)

### NFRA Operational Requirements

**Availability**:
- Uptime: 99.5% (43.8 hours downtime/year allowed)
- Maintenance Window: Sundays 2-6 AM

**Data Retention**:
- Processed Reports: 10 years (archive to tape)
- Raw PDFs: Permanent
- System Logs: 5 years

**Audit Trail**:
- Every action logged (Cert-In requirement)
- Logs tamper-proof (write-only table)
- Export capability for RTI requests

---

## Success Metrics (Measurable)

### Technical Performance
- OCR Accuracy: >98% (measured via CER)
- Table Extraction: >95% field-level match
- Processing Speed: 95% of reports under 10 minutes
- System Uptime: >99.5%

### Business Impact
- Manual Review Time: Reduced from 4 hours to 30 minutes (8x speed-up)
- Document Coverage: From 100 reports/quarter to 1000+ reports/quarter
- Error Detection: Flag 80% of known violations (vs 60% manual catch rate)

### User Satisfaction
- NFRA officer training completion: 100%
- System satisfaction score: >4/5
- Help desk resolution time: <4 hours (95th percentile)
