# 02. PROJECT CODE STRUCTURE & ARCHITECTURE

This document defines the physical directory structure for the AI-FRC "Digital Auditor" codebase. This structure follows clean architecture principles, separating the **Vision Layer (Reading)**, **Logic Layer (Auditing)**, and **Inference Layer (LLM)**.

---

## Directory Hierarchy

```text
/AI-FRC
├── data/
│   ├── raw/                # Original PDFs downloaded from BSE India (T0.4)
│   ├── benchmarks/         # Global datasets (FinTabNet, DocLayNet) (T0.3)
│   ├── processed/          # Intermediate JSONs, extracted text, and tables
│   └── ground_truth/       # Manually verified Excel/JSON Benchmarks (T0.5)
├── src/
│   ├── vision/             # THE EYES: OCR & Document Layout Analysis
│   │   ├── ocr/            # PaddleOCR integration & wrappers
│   │   ├── extraction/     # Table detection and cell-parsing logic
│   │   └── mapper/         # Document segmentation (Finding Balance Sheets)
│   ├── compliance/         # THE BRAIN: Regulatory Audit Rules
│   │   ├── engines/        # IndAS rule implementations
│   │   ├── analytics/      # Financial ratio & trend calculations
│   │   └── schema/         # Unified JSON schemas for audit data
│   ├── inference/          # THE VOICE: LLM & RAG Infrasctructure
│   │   ├── vllm_worker/    # Mistral/Llama-3 serving logic
│   │   ├── rag/            # Embedding, Vector DB (Qdrant) logic
│   │   └── prompts/        # System prompts for "Insight Bot"
│   ├── api/                # THE NERVE SYSTEM: FastAPI Endpoints
│   │   ├── routes/         # REST API definitions
│   │   ├── middleware/     # Auth, Logging, PII Redaction
│   │   └── workers/        # Celery/RabbitMQ task orchestration
│   └── web/                # THE FACE: GIGW 3.0 Compliant UI (Next.js)
├── infra/
│   ├── docker/             # Dockerfiles & Compose for air-gapped setup
│   ├── k8s/                # Helm charts for MeitY/NIC cloud
│   └── scripts/            # Setup scripts (GPU check, Model pull)
├── tests/
│   ├── unit/               # Core logic testing
│   ├── validation/         # Accuracy testing scripts (CER/F1)
│   └── load/               # Locust scripts for performance testing
└── .docs/                  # Internal technical documentation
```

---

## Core Engineering Principles

### 1. The "Hybrid-Inference" Pattern
The system MUST detect hardware at runtime.
*   **Location**: `src/inference/config.py`
*   **Logic**: 
    - If `torch.cuda.is_available()`: Load `Llama-3-70B` (Server variant).
    - Else: Load `Llama-3-8B-GGUF` or `OmniParser-Small` (CPU/ONNX variant).
    - *Purpose*: Prevents development blocking due to missing GPU drivers.

### 2. The "Citation-First" Rule
No data enters the Compliance Engine without a **Source URI**.
*   **Format**: `{"value": 500.5, "unit": "Cr", "source": {"page": 45, "bbox": [x1, y1, x2, y2]}}`
*   *Purpose*: Ensures every audit flag is defensible and visually traceable.

### 3. PII-at-Source Redaction
PII (PAN, Signatures) should be identified by the `vision` layer and redacted before hitting the `inference` layer vector database.

---

## Next Steps for Implementation (T0.1)

1. **Initialize Git**: `git init` in `/AI-FRC`.
2. **Create Directories**: Run the scaffolding script to generate the above folders.
3. **Environment Setup**: Define `requirements.txt` and `Dockerfile` for the CPU-fallback mode.
