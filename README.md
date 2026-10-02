# 🛡️ OPERATION ABHEDYA-CHAKRA (अभैद्य चक्र)
### Intelligent Money Mule Ring Detection & Digital Forensics Platform

**Operation Abhedya-Chakra** is an end-to-end, locally deployable cybercrime analytics and financial forensics platform engineered for law enforcement agencies, cybercrime investigation cells, and banking fraud risk units.

Built to ingest and analyze **2,000,000+ banking transaction records** on commodity hardware (16 GB RAM) without Out-Of-Memory (OOM) failures, it uses a high-performance **DuckDB columnar B-tree indexing engine**, time-aware graph traversal, explainable 0–100 Mule Risk scoring, and strict anti-hallucination evidentiary grounding.

---

## 🏆 Core Judging Targets & Capabilities

### 1. Blind Victim Query Test (Highest Priority)
- **Arbitrary Victim Ingestion:** Enter any unknown victim account ID to instantaneously trace downstream illicit fund movement up to **4 hops**.
- **Deterministic 4-Hop Hierarchy:**
  - **Layer 1 (Collector Mules):** High fan-in aggregation from multiple victims.
  - **Layer 2 (Distributor Mules):** High fan-out rapid dispersion across downstream intermediaries.
  - **Layer 3 (Terminal Cash-Out Nodes):** Wallets, crypto/P2P exchanges, emulator/script endpoints.
- **Microsecond Time Causality:** Guarantees downstream transaction timestamp $T_{\text{out}} \ge T_{\text{in}}$.
- **Money Conservation:** Preserves exact database transaction IDs, dates, payment channels, and rupee amounts.
- **Sub-Second Traversal Latency:** **~130 ms** 4-hop graph extraction (well below the $\le 2\text{s}$ hackathon benchmark).

### 2. 0–100 Explainable Mule Risk Index
- Hybrid scoring based on configurable weights in [config/detection.yaml](file:///c:/Users/VICTUS/OneDrive/Desktop/void%20hack8.0/config/detection.yaml):
  - High-Velocity Pass-Through ($\ge 85\text{--}90\%$ dispersed in 3–30 mins)
  - Fan-in & Fan-out degree centralities
  - Cyber & device fingerprints (`Web_Emulator`, `Linux_Script`, proxy IPs)
  - Narration markers (`crypto`, `usdt`, `p2p`, `commission`, `task_reward`)
- Categorized into: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.

### 3. Anti-Hallucination & Statutory LEO Reports
- **100% Database-Verified Claims:** Before any report is rendered, every account, amount, and transaction ID is verified against DuckDB.
- **Police Case Diary:** Chronological investigation audit report.
- **Section 91 Cr.P.C. / Section 94 BNSS Bank Freeze Requisition:** Statutory draft notice ready for dispatch to bank nodal officers.
- **Prompt Injection Defense:** Sanitizes adversarial text in transaction remarks (e.g. *"Ignore previous instructions..."* is treated strictly as unexecutable data).

---

## 📁 Project Architecture & File Structure

```
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI server (Victim queries, dataset status, reports)
│   ├── storage/
│   │   └── db.py                # High-performance DuckDB columnar storage & B-tree indexes
│   ├── ingestion/
│   │   └── normalizer.py        # Chunked streaming (50k rows/chunk), error-tolerant parser
│   ├── detection/
│   │   └── engine.py            # Pass-through velocity, fan-in/out, 0-100 risk score, L1/L2/L3 classifier
│   ├── graph/
│   │   └── trail_engine.py      # Indexed 4-hop time-aware money trail graph engine
│   ├── evidence/
│   │   └── grounding.py         # Anti-hallucination verification against physical DB records
│   ├── reports/
│   │   └── generator.py         # Police Case Diary & Section 91 CrPC / BNSS freeze notice generator
│   ├── ai/
│   │   └── case_officer.py      # Local AI Case Officer with prompt injection shield
│   └── analytics/
│       └── evaluation.py        # Ground-truth evaluation (Precision, Recall, F1, FPR, Confusion Matrix)
├── config/
│   ├── detection.yaml           # Configurable thresholds, weights, and cyber signal lists
│   └── dataset_schema.yaml      # Dynamic schema mapping adapter for external CSV headers
├── frontend/
│   └── index.html               # Forensic LEO dashboard with interactive Vis-Network graph
├── scripts/
│   ├── generate_synthetic_data.py # Synthesizes multi-tier laundering rings + retail noise
│   ├── ingest_dataset.py        # CLI dataset streaming ingestion command
│   ├── investigate_victim.py    # CLI blind victim trace tool
│   └── benchmark.py             # Performance & concurrency benchmark suite
├── tests/
│   └── test_pipeline.py         # Automated test suite (7 comprehensive test suites)
├── data/
│   ├── raw/                     # External raw dataset storage
│   ├── processed/               # DuckDB analytical database (`abhedya_chakra.duckdb`)
│   ├── index/                   # Graph indexes
│   └── cache/                   # Query & investigation cache
├── reports/                     # Generated Case Diaries & Statutory Freeze Notices
├── requirements.txt             # Pinned production dependencies
└── README.md                    # Platform documentation
```

---

## ⚡ Quick Start Guide

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Run Automated Test Suite
Verify all 7 forensic test suites (ingestion, 4-hop tracing, causality, layer classification, anti-hallucination, prompt injection defense, statutory notices):
```bash
python -m pytest tests/test_pipeline.py -v
```
*(All 7 tests execute and pass in ~1.15 seconds!)*

### 3. Run Benchmark Suite
```bash
python scripts/benchmark.py
```
**Benchmark Highlights:**
- **Throughput:** ~52,800 rows/second
- **Account 360 Latency:** ~2.6 ms
- **4-Hop Trail Traversal Latency:** ~130 ms (Target: $\le 2000\text{ ms}$)
- **Peak RAM Footprint:** ~126 MB (Well below the 16 GB limit)

---

## 🚀 Running the Platform

### Launch the Web Forensics Dashboard
Start the local FastAPI server:
```bash
python -m uvicorn backend.api.main:app --port 8000 --host 127.0.0.1
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**

---

## 🎯 How to Demonstrate to Judges (Demo Flow)

1. **Open the Dashboard** at `http://localhost:8000`.
2. **Review Dataset Status:** Click **"📁 Dataset Ingestion & Status"** to view current indexed records, volume, and date range. If empty, click **"🎲 Generate & Index Demo Dataset"** to synthesize 25,000 multi-tier records.
3. **Execute Blind Victim Query:**
   - In the search bar, enter victim account ID `V_ACC_1001` (or click one of the quick pill buttons).
   - Click **"⚡ Trace 4-Hop Money Trail"**.
   - Note the sub-second query latency badge (`⚡ 4-Hop Query Latency: ~130 ms`).
4. **Inspect Visual 4-Hop Graph:**
   - Notice the hierarchical layout: **Victim** (Cyan) $\rightarrow$ **Layer 1 Collector** (Amber) $\rightarrow$ **Layer 2 Distributor** (Orange) $\rightarrow$ **Layer 3 Terminal Cash-Out** (Rose).
   - Hover and click any edge to see the exact ₹ amount and Transaction ID.
5. **Account 360 Forensic Inspector:**
   - Click on `C_ACC_5001` or `D_ACC_6001` to view its **0–100 Mule Risk Index**, pass-through ratio, and device anomalies.
6. **Local AI Case Officer Briefing:**
   - Review the AI narrative grounded in 100% verified facts.
7. **Generate Legal Documents:**
   - Click **"📄 Police Case Diary & Freeze Notices"** to view the auto-generated Police Case Diary and statutory Section 91 Cr.P.C. Bank Freeze Requisition notice.

---

## 📥 Ingesting Your 2,000,000-Row Dataset

When your actual hackathon dataset is ready, ingest it without changing any code:

### Option A: Via Command Line (Recommended for Large Files)
```bash
python scripts/ingest_dataset.py --file path/to/your_2M_dataset.csv --chunk-size 50000 --reset-db
```
- Streams 50,000 rows per chunk.
- Displays live throughput (rows/sec), valid vs rejected rows, and builds B-tree graph indexes automatically.

### Option B: Via Web UI
1. Navigate to **"📁 Dataset Ingestion & Status"** in the web app.
2. Select your CSV or Parquet file and click **"Stream Ingestion into DuckDB"**.

### Custom Schema Mapping
If your dataset uses different column names (e.g., `From_Acc` instead of `Sender_Account`), configure the mapping in [config/dataset_schema.yaml](file:///c:/Users/VICTUS/OneDrive/Desktop/void%20hack8.0/config/dataset_schema.yaml).

---

## 💻 CLI Blind Victim Investigation
To run an instant investigation directly from the terminal:
```bash
python scripts/investigate_victim.py --victim V_ACC_1001 --hops 4 --generate-reports
```

---

## 🛡️ Anti-Hallucination & Security Architecture

1. **Deterministic Grounding:** No LLM is ever used to query raw data or invent transaction paths. Every displayed edge is directly queried from DuckDB B-tree indexes.
2. **Prompt Injection Shield:** All narration strings, remarks, and user metadata are HTML-escaped and filtered for adversarial commands (*"ignore previous instructions"*, *"admin override"*, etc.).
3. **Completely Local & Offline:** No external API keys or cloud dependencies required. Financial data never leaves your machine.
