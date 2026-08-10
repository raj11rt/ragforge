# 🚀 RAGForge

**Automated RAG Pipeline Optimization & Multi-Metric Benchmarking Platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-61DAFB?style=for-the-badge&logo=chromadb)](https://github.com/chroma-core/chroma)
[![Ragas](https://img.shields.io/badge/RAGAS-FF6F00?style=for-the-badge)](https://github.com/explodinggradients/ragas)

RAGForge is an automated optimization platform designed to solve the "trial-and-error" dilemma of building Retrieval-Augmented Generation (RAG) applications. Instead of guessing parameters, RAGForge automatically benchmarks multiple pipeline configurations (varying chunk sizes, embedding models, and retrieval depths), scores them using multi-metric evaluations, and ranks them on an interactive leaderboard.

---

## 💡 The Problem

Most developers build RAG pipelines by guessing core parameters:
* *Which chunk size (512 vs. 1024) retrieves the most contextually rich information?*
* *Which embedding model provides the highest vector similarity matching?*
* *How many chunks (`top_k`) should be retrieved for optimal generation quality?*

RAGForge replaces subjective guessing with **data-driven benchmarking**.

---

## ✨ Features

### 📂 Document Processing
* **PDF Ingestion & Text Extraction**: Automatic PDF processing and raw text extraction.
* **Granular Chunking**: Parametric splitting based on token configurations.
* **Persistent Document Registry**: Extracted text database storage mapped by unique document IDs.

### ⚙️ Benchmarking Engine
* **Multi-Configuration Testing**: Benchmarks pipelines concurrently across a configurable parameters matrix.
* **Asynchronous Execution**: Uses FastAPI background worker tasks to execute heavy evaluations without timing out.
* **ChromaDB Vector Store isolation**: Automatically provisions and tears down temporary vector indexes for each run.

### 🧪 Multi-Metric Evaluation (RAGAS-aligned)
Calculates scores for every generated response across four key dimensions:
| Metric | Description | What it detects |
| :--- | :--- | :--- |
| **Faithfulness** | Measures how grounded the answer is in the retrieved context. | Hallucinations |
| **Answer Relevancy** | Evaluates how directly the generated answer addresses the question. | Off-topic or generic LLM replies |
| **Context Precision** | Measures the proportion of relevant chunks in the retrieved context. | Retrieval noise or clutter |
| **Context Recall** | Checks if all the required information to answer is present in the context. | Incomplete retrieval |
| **Overall Score** | The harmonic mean of the four dimensions. | Overall pipeline quality |

### 🖥️ Interactive Streamlit Dashboard
* **📂 Upload & Run**: Real-time polling interface showing status tracking (`PENDING` -> `RUNNING` -> `COMPLETED`).
* **🏆 Leaderboard**: Ranked table highlighting the winning pipeline configuration.
* **📊 Analytics Charts**: Altair-powered visualization of parameters to identify top-performing chunk sizes and models.
* **🔍 Past Experiments & CSV Export**: Review detailed question-answer-context tables and download them as CSV reports.

---

## 🛠️ Tech Stack

* **Backend API**: FastAPI, Uvicorn
* **Database**: PostgreSQL (SQLAlchemy ORM)
* **Vector Store**: ChromaDB (Persistent client)
* **LLM & Embeddings**: LangChain Google GenAI (Gemini-2.5-Flash), HuggingFace Embeddings (`sentence-transformers/all-MiniLM-L6-v2`, `BAAI/bge-small-en-v1.5`)
* **Frontend**: Streamlit
* **Environment & Package Manager**: UV, dotenv

---

## 📂 Project Structure

```text
ragforge/
│
├── app/
│   ├── api/                   # FastAPI route definitions
│   │   ├── benchmarks.py      # Async benchmark task trigger
│   │   ├── documents.py       # PDF uploading and processing
│   │   ├── experiments.py     # Experiment listing & detailed results
│   │   └── leaderboard.py     # Leaderboard endpoint
│   │
│   ├── benchmark/             # Core benchmarking runner
│   │   ├── runner.py          # Benchmark pipeline executor
│   │   └── config_generator.py# Active configurations matrix
│   │
│   ├── db/                    # PostgreSQL models & repositories
│   ├── evaluation/            # RAGAS metrics implementation
│   ├── rag/                   # Chunker, vector store, and generator services
│   └── main.py                # FastAPI app startup
│
├── tests/                     # Unit test suite (pytest)
│   ├── test_database.py       # DB schema & repository tests
│   └── test_evaluator.py      # Evaluation metric tests
│
├── dashboard.py               # Streamlit Dashboard application
├── create_tables.py           # Table initialization script
├── manual_test_leaderboard.py # Manual command-line script
├── pyproject.toml             # UV dependency specification
└── assets/                    # Dashboard screenshots and images
```

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/raj11rt/ragforge.git
cd ragforge
```

### 2. Install Dependencies
Ensure you have `uv` installed, then synchronize the environment:
```bash
uv sync
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/ragforge
```

### 4. Initialize Database Tables
Create the necessary PostgreSQL tables:
```bash
uv run python create_tables.py
```

---

## 🐳 Running with Docker

You can run the entire stack (PostgreSQL database, FastAPI backend, and Streamlit dashboard) with a single command using Docker Compose:

### 1. Configure Environment Variables
Create a `.env` file in the root directory (if you haven't already) and add your Gemini API Key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```
*(Note: You do not need to configure `DATABASE_URL` for Docker, as it is preconfigured in `docker-compose.yml` to route to the PostgreSQL service container).*

### 2. Start the Stack
Run the following command to build and launch all services:
```bash
docker compose up --build
```

Once all containers are running:
* **Streamlit Frontend Dashboard**: Access at [http://localhost:8501](http://localhost:8501)
* **FastAPI Interactive Docs**: Access at [http://localhost:8000/docs](http://localhost:8000/docs)
* **PostgreSQL Database**: Port `5432` is exposed on your local machine.

Database tables are automatically created on startup, so no manual table initialization is needed!

### 3. Stop the Stack
To stop the services and retain database volume data:
```bash
docker compose down
```
To also remove database volume data:
```bash
docker compose down -v
```

---

## 🏃 Running the Application (Local Installation)

To run the application locally, you will need to start the FastAPI backend and the Streamlit dashboard:

### 1. Start the FastAPI Server
```bash
uv run uvicorn app.main:app --port 8000
```
*The API interactive docs will be available at `http://127.0.0.1:8000/docs`.*

### 2. Start the Streamlit Dashboard
```bash
uv run streamlit run dashboard.py
```
*Access the UI in your browser at `http://localhost:8501`.*

### 3. Run the Unit Test Suite
```bash
uv run pytest
```

## 📸 Screenshots

#### 1. System Architecture Diagram
![System Architecture](assets/architecture.png)
*Relationship between the Dashboard, FastAPI, PostgreSQL, ChromaDB, and Google Gemini LLM.*

#### 2. Tab 1 - Upload & Run
![Upload & Run](assets/dashboard_upload_run.png)
*Document statistics cards and the real-time background status polling loader.*

#### 3. Tab 2 - Leaderboard
![Leaderboard](assets/dashboard_leaderboard.png)
*Ranked configuration leaderboard and the highlight banner marking the winning config.*

#### 4. Tab 3 - Analytics Charts
![Analytics Charts](assets/dashboard_charts.png)
*Score metric breakdowns visualized using interactive charts.*

#### 5. Tab 4 - Detailed Results & Export
![Detailed Results & Export](assets/dashboard_details.png)
*Detailed question-answer-metric table and the CSV download trigger.*

---

## 🔬 Benchmark Configuration Matrix

RAGForge evaluates the following parameter combinations automatically for each uploaded file:

* **Embedding Models**:
  - `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional)
  - `BAAI/bge-small-en-v1.5` (384-dimensional, highly retrieval-focused)
* **Chunk Sizes & Overlaps**:
  - `512` token chunks with a `50` token overlap.
  - `1024` token chunks with a `100` token overlap.
* **Retrieval Depth (`top_k`)**:
  - Top `4` retrieved contexts.
  - Top `5` retrieved contexts.

---

## 👨‍💻 Author

**Raj Tiwari**
*B.Tech Computer Science | AI Engineer Aspirant*

---

## ⭐ Why RAGForge?

Most RAG projects focus purely on generating answers. RAGForge shifts the perspective towards quality assurance. By automating pipeline configuration evaluation, experiment tracking, and metric scoring, RAGForge provides the metrics needed to deploy production-grade RAG systems.
