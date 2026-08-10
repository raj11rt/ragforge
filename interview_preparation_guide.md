# 🚀 Interview Preparation & Demo Guide: RAGForge

This guide walks you through how to run **RAGForge** from basic prerequisites and presents a step-by-step framework to demonstrate it to an interviewer.

---

## 💻 Part 1: How to Run the Project (From Scratch)

You can run the project either **Locally (Recommended if Docker is off)** or via **Docker**.

### Method A: Local Installation (Fastest if Postgres is already installed)

#### 1. Setup Prerequisites
* **Python 3.11+** installed on your system.
* **uv** (high-performance Python package manager). If not installed:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
* **PostgreSQL** running on your local machine at port `5432`.

#### 2. Configure Environment Variables
Create a `.env` file in the root of the `ragforge` directory:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key
DATABASE_URL=postgresql://postgres:postgre123@localhost:5432/ragforge
```

#### 3. Install Dependencies & Build Virtual Environment
Use `uv` to automatically sync dependencies defined in `pyproject.toml`:
```bash
uv sync
```

#### 4. Create Database Tables
Initialize the database tables:
```bash
uv run python create_tables.py
```

#### 5. Run the Servers
You need to open two terminal windows (or run them in the background):
* **Terminal 1: Start FastAPI Backend**
  ```bash
  uv run uvicorn app.main:app --port 8000
  ```
* **Terminal 2: Start Streamlit Frontend Dashboard**
  ```bash
  uv run streamlit run dashboard.py
  ```

*Access the Dashboard at [http://localhost:8501](http://localhost:8501) and API docs at [http://localhost:8000/docs](http://localhost:8000/docs).*

---

### Method B: Docker & Docker Compose Installation

If Docker Desktop is running, you can launch everything in one command without installing Python or Postgres locally:

1. Create a `.env` file with just your API key:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key
   ```
2. Run:
   ```bash
   docker compose up --build
   ```
   *(Note: This automatically spins up Postgres, the FastAPI Backend with auto-migration tables creation, and the Streamlit frontend. It also routes internal database and backend URLs automatically).*

---

## 🎤 Part 2: The Interview Demo Flow (Screen-Share Script)

Follow this structure during your live demo to tell a compelling story.

### 1. The Hook: The "Why" (30 Seconds)
> *"Most developers build RAG (Retrieval-Augmented Generation) applications using guesswork. They guess chunk sizes, embedder models, and how many chunks to retrieve. RAGForge replaces guesswork with metrics-driven benchmarking. It lets developers upload a document, benchmark multiple combinations of chunk sizes and embedders, and outputs a ranked leaderboard based on RAGAS-aligned metrics."*

### 2. Walkthrough Steps
* **Step 1: Upload a PDF (Tab 1)**: Upload a document and hit **Start Benchmark Suite**. Explain that the backend handles this asynchronously using FastAPI background tasks so the client never times out on heavy LLM evaluations.
* **Step 2: The Leaderboard (Tab 2)**: Show them the completed experiment. Show how the winning combination is highlighted at the top based on its overall score.
* **Step 3: Explaining the Metrics**: Show that you aren't just measuring speed, but **RAG Quality**:
  * **Faithfulness**: Are there hallucinations? (Is the answer grounded in context?)
  * **Answer Relevancy**: Does the answer actually address the user's prompt?
  * **Context Recall**: Did the retriever extract all necessary information from the document?
  * **Context Precision**: Did the retriever fetch clean, relevant chunks without introducing noise?
* **Step 4: Analytics Charts (Tab 3)**: Use the Altair charts to show parameter trends (e.g., *"We can see that chunk size 512 results in higher faithfulness, but lower recall compared to chunk size 1024."*).
* **Step 5: Export (Tab 4)**: Show that they can export the raw scoring dataset to CSV for further team audits.

---

## 🧠 Part 3: Anticipated Technical Questions & Answers

Be prepared to answer these engineering design choices:

#### Q: How do you handle vector store isolation so different configurations don't corrupt each other?
> **Answer**: *"For each config tested in a run, we programmatically create a unique, isolated ChromaDB collection. We process the chunks, run the embeddings, store them, retrieve, generate answers, and then clean up the transient collections when finished. This ensures zero data contamination between different parameter tests."*

#### Q: Why did you use PostgreSQL instead of just storing everything in ChromaDB?
> **Answer**: *"ChromaDB is optimized for high-dimensional vector search. But for logging experiment runs, tracking configurations, and structured leaderboard tabular metrics, relational databases like PostgreSQL are much more appropriate. We use SQLAlchemy to map results to Postgres tables, which allows us to write fast, complex queries for the leaderboard."*

#### Q: How does the app handle heavy, long-running RAGAS evaluations without freezing?
> **Answer**: *"We run the benchmarking engine as an asynchronous FastAPI background task. When the frontend requests a run, the API immediately returns a unique `experiment_id` and a `PENDING` status. The frontend then polls the backend status endpoint while the background task runs in a separate thread. This provides a smooth UI experience."*
