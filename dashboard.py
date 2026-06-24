import streamlit as st
import requests

st.set_page_config(
    page_title="RAGForge",
    layout="wide"
)

st.title("🚀 RAGForge")

st.write(
    "Automated RAG Optimization & Benchmarking Platform"
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# Upload only once
if uploaded_file and "document_id" not in st.session_state:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    response = requests.post(
        "http://localhost:8000/documents/upload",
        files=files
    )

    if response.status_code == 200:

        data = response.json()

        st.session_state["document_id"] = data["document_id"]
        st.session_state["pages"] = data["pages"]
        st.session_state["chunks"] = data["chunks_created"]
        st.session_state["characters"] = data["characters"]

# Display uploaded document info
if "document_id" in st.session_state:

    st.success("Document uploaded successfully")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Pages",
        st.session_state["pages"]
    )

    col2.metric(
        "Chunks",
        st.session_state["chunks"]
    )

    col3.metric(
        "Characters",
        st.session_state["characters"]
    )

    st.code(
        st.session_state["document_id"],
        language=None
    )

    st.divider()

    st.subheader("Run Benchmark")
    

    if st.button("Run Benchmark"):

        response = requests.post(
            "http://localhost:8000/benchmarks/run",
            params={
                "document_id":
                st.session_state["document_id"]
            }
        )

        st.success("Benchmark request sent")
        st.divider()
        st.subheader("🏆 Leaderboard")
        leaderboard = requests.get(
            "http://localhost:8000/leaderboard"
        )

        if leaderboard.status_code == 200:
            st.dataframe(
            leaderboard.json(),
            use_container_width=True
        )

        st.json(
            response.json()
        )