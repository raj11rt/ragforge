# 🚀 RAGForge

**Automated RAG Optimization & Benchmarking Platform**

RAGForge is a platform for evaluating and optimizing Retrieval-Augmented Generation (RAG) pipelines. Instead of manually experimenting with chunk sizes, embedding models, and retrieval settings, RAGForge automatically benchmarks multiple configurations, evaluates their performance, and stores results for comparison.

---

##  Problem Statement

Most RAG applications are built using trial and error:

* Which chunk size works best?
* Which embedding model retrieves the most relevant context?
* How many documents should be retrieved?
* Which configuration produces the highest-quality answers?

Developers often guess these values and deploy without systematic evaluation.

RAGForge solves this problem by automatically generating and benchmarking multiple RAG configurations, allowing developers to identify the best-performing setup using measurable results.

---

##  Features

### Document Processing

* PDF Upload
* Text Extraction
* Document Storage
* Metadata Tracking

### Retrieval Pipeline

* Configurable Chunk Size
* Configurable Chunk Overlap
* Multiple Embedding Models
* Vector Search with ChromaDB
* Top-K Retrieval

### Benchmarking Engine

* Multi-Configuration Testing
* Automated Retrieval Evaluation
* Answer Generation
* Experiment Tracking
* Leaderboard Ranking

### Dashboard

* Upload Documents
* Run Benchmarks
* View Leaderboard
* Experiment History
* Experiment Details

---

##  Architecture

![Architecture](assets/architecture.png)

### High-Level Flow

```text
User
 │
 ▼
Streamlit Dashboard
 │
 ▼
FastAPI Backend
 │
 ├── Upload API
 ├── Benchmark API
 ├── Experiments API
 └── Leaderboard API
 │
 ▼
Benchmark Runner
 │
 ├── Chunking
 ├── Embedding
 ├── Retrieval
 ├── Generation
 └── Evaluation
 │
 ▼
PostgreSQL

 ▲
 │
ChromaDB
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL

### RAG Components

* ChromaDB
* LangChain
* HuggingFace Embeddings
* Google Gemini

### Frontend

* Streamlit

### Infrastructure

* Docker
* Docker Compose
* UV Package Manager

---

## 📂 Project Structure

```text
ragforge/
│
├── app/
│   ├── api/
│   ├── benchmark/
│   ├── db/
│   ├── evaluation/
│   ├── rag/
│   ├── services/
│   └── storage/
│
├── dashboard.py
├── create_tables.py
├── run_benchmark.py
│
├── Dockerfile
├── docker-compose.yml
│
├── pyproject.toml
├── uv.lock
│
└── assets/
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone <https://github.com/raj11rt/ragforge>
cd ragforge
```

### Install Dependencies

```bash
uv sync
```

### Configure Environment

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/ragforge
```

### Create Database Tables

```bash
uv run python create_tables.py
```

### Start FastAPI

```bash
uv run uvicorn app.main:app --reload
```

### Start Dashboard

```bash
uv run streamlit run dashboard.py
```

---

## 📊 API Endpoints

### Documents

```http
POST /documents/upload
```

Upload and process PDF documents.

### Benchmarks

```http
POST /benchmarks/run
```

Run benchmark experiments.

### Experiments

```http
GET /experiments
POST /experiments
GET /experiments/{id}
GET /experiments/{id}/results
```

### Leaderboard

```http
GET /leaderboard
```

Retrieve ranked benchmark results.

---

## 📸 Screenshots

### Dashboard

![Dashboard](assets/dashboard.png)

### Leaderboard

![Leaderboard](assets/leaderboard.png)

### Experiment History

![Experiments](assets/experiments.png)

### Experiment Details

![Experiment Details](assets/experiment_details.png)

---

## 🔬 Current Benchmark Parameters

RAGForge currently benchmarks:

* Chunk Size
* Chunk Overlap
* Top-K Retrieval
* Embedding Models

Example embedding models:

* sentence-transformers/all-MiniLM-L6-v2
* BAAI/bge-small-en-v1.5

---

## 🔮 Future Improvements

* RAGAS Integration
* Background Benchmark Jobs
* Redis Queue
* Progress Tracking
* Benchmark Comparison Charts
* Multi-Document Evaluation
* Advanced Metrics Dashboard
* Export Benchmark Reports

---

## 👨‍💻 Author

Raj Tiwari

B.Tech Computer Science | AI Engineer Aspirant

---

## ⭐ Why RAGForge?

Most RAG projects focus on answering questions.

RAGForge focuses on answering a more important question:

> Which RAG pipeline configuration actually performs best?

By automating benchmarking, experiment tracking, and result comparison, RAGForge helps developers build more reliable and measurable RAG systems.
