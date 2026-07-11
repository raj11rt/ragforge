import time
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="RAGForge Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Aesthetics
st.markdown("""
<style>
    /* Dark Theme Accent & Card Styles */
    .stApp {
        background-color: #0B0F19;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #6366F1;
    }
    .metric-card h3 {
        margin: 0;
        color: #94A3B8;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card p {
        margin: 10px 0 0 0;
        color: #F8FAFC;
        font-size: 26px;
        font-weight: bold;
    }
    .title-gradient {
        background: linear-gradient(to right, #6366F1, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #94A3B8;
        font-size: 16px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="title-gradient" style="font-size: 28px;">RAGForge</div>', unsafe_allow_html=True)
    st.write("Automated RAG Optimization & Evaluation")
    st.divider()
    st.markdown("### 🔬 RAGAS Metrics Defined")
    st.markdown("""
    - **Faithfulness**: Is the answer grounded purely in the context? (No hallucinations)
    - **Answer Relevancy**: Does the answer directly address the question?
    - **Context Precision**: Did the retriever fetch relevant chunks?
    - **Context Recall**: Did the retriever capture all necessary information?
    """)
    st.divider()
    st.info("Ensure the FastAPI backend is running at `http://127.0.0.1:8000`.")

# Main Title
st.markdown('<div class="title-gradient">🚀 RAGForge Optimization Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Evaluate embedding models, chunk sizes, and retrieval depths to identify the best pipeline configuration.</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Upload & Run", 
    "🏆 Leaderboard", 
    "📊 Analytics Charts", 
    "🔍 Experiment Details & Export"
])

# FastAPI Base URL
BACKEND_URL = "http://127.0.0.1:8000"


# ==========================================
# TAB 1: UPLOAD & RUN
# ==========================================
with tab1:
    st.header("📂 Document Processing & Benchmark Runner")
    
    col_upload, col_stats = st.columns([2, 3])
    
    with col_upload:
        uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
        if uploaded_file and "document_id" not in st.session_state:
            with st.spinner("Processing PDF, extracting text, and generating base chunks..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/documents/upload", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["document_id"] = data["document_id"]
                        st.session_state["filename"] = data["filename"]
                        st.session_state["pages"] = data["pages"]
                        st.session_state["chunks"] = data["chunks_created"]
                        st.session_state["characters"] = data["characters"]
                        st.success("File uploaded and base indexing completed successfully!")
                    else:
                        st.error(f"Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
                    
    with col_stats:
        if "document_id" in st.session_state:
            st.markdown(f"#### Active Document: `{st.session_state['filename']}`")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown('<div class="metric-card"><h3>Total Pages</h3><p>{}</p></div>'.format(st.session_state["pages"]), unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="metric-card"><h3>Base Chunks</h3><p>{}</p></div>'.format(st.session_state["chunks"]), unsafe_allow_html=True)
            with c3:
                st.markdown('<div class="metric-card"><h3>Characters</h3><p>{}</p></div>'.format(st.session_state["characters"]), unsafe_allow_html=True)
                
            st.text_input("Active Document ID (Internal)", st.session_state["document_id"], disabled=True)
            
            st.divider()
            st.subheader("Run Multi-Config Benchmark")
            st.write("Triggers evaluations across 4 configurations (various chunk sizes and embedding models). This runs asynchronously in the backend.")
            
            if st.button("🚀 Start Benchmark Suite", type="primary"):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/benchmarks/run", 
                        params={"document_id": st.session_state["document_id"]}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["active_experiment_id"] = data["experiment_id"]
                        st.success(f"Benchmark started! Experiment ID: {data['experiment_id']}")
                    else:
                        st.error(f"Could not trigger benchmark: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.info("Upload a PDF document to begin.")

    # Status Polling Box
    if "active_experiment_id" in st.session_state:
        st.divider()
        st.subheader("🔄 Real-Time Run Progress")
        
        status_box = st.empty()
        exp_id = st.session_state["active_experiment_id"]
        
        # Poll state
        polling = True
        while polling:
            try:
                res = requests.get(f"{BACKEND_URL}/experiments/{exp_id}")
                if res.status_code == 200:
                    exp_data = res.json()
                    status = exp_data.get("status", "PENDING")
                    
                    if status == "RUNNING":
                        status_box.info(f"⏳ Experiment **#{exp_id}** is currently running models and scoring via RAGAS. Please hold on...")
                    elif status == "COMPLETED":
                        status_box.success(f"✅ Experiment **#{exp_id}** completed successfully! Head over to the Leaderboard tab to view the results.")
                        polling = False
                    elif status == "FAILED":
                        status_box.error(f"❌ Experiment **#{exp_id}** failed during execution. Check backend console logs.")
                        polling = False
                    else:
                        status_box.warning(f"🕒 Experiment **#{exp_id}** is pending in the queue...")
                else:
                    status_box.error(f"Could not poll status: Server returned code {res.status_code}")
                    polling = False
            except Exception as e:
                status_box.error(f"Polling connection error: {e}")
                polling = False
                
            if polling:
                time.sleep(2.5)

# ==========================================
# TAB 2: LEADERBOARD
# ==========================================
with tab2:
    st.header("🏆 RAG Configuration Leaderboard")
    st.write("Aggregated ranking of configurations based on average overall evaluation scores.")
    
    if st.button("🔄 Refresh Leaderboard"):
        st.rerun()

    try:
        response = requests.get(f"{BACKEND_URL}/leaderboard")
        if response.status_code == 200:
            leaderboard_data = response.json()
            if leaderboard_data:
                df_lead = pd.DataFrame(leaderboard_data)
                
                # Highlight the winner
                winner = df_lead.iloc[0]
                st.balloons()
                st.success(
                    f"🥇 **Best Performing Config:** {winner['config_name']} "
                    f"(Score: **{winner['average_score']}** | "
                    f"Faithfulness: **{winner['faithfulness']}** | "
                    f"Answer Relevancy: **{winner['answer_relevancy']}**)"
                )
                
                # Format dataframe columns
                df_display = df_lead.rename(columns={
                    "config_name": "Pipeline Configuration",
                    "chunk_size": "Chunk Size",
                    "chunk_overlap": "Overlap",
                    "top_k": "Top-K",
                    "average_score": "Overall Score (Avg)",
                    "answer_relevancy": "Answer Relevancy (Avg)",
                    "faithfulness": "Faithfulness (Avg)",
                    "context_precision": "Context Precision (Avg)",
                    "context_recall": "Context Recall (Avg)"
                })
                
                st.dataframe(df_display, use_container_width=True)
            else:
                st.info("No benchmark results found. Run a benchmark first to populate the leaderboard.")
        else:
            st.error(f"Failed to fetch leaderboard data: {response.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")

# ==========================================
# TAB 3: ANALYTICS CHARTS
# ==========================================
with tab3:
    st.header("📊 Visualization & Parameter Analytics")
    st.write("Inspect how different chunk sizes and embedding models directly impact evaluation dimensions.")
    
    try:
        response = requests.get(f"{BACKEND_URL}/leaderboard")
        if response.status_code == 200:
            leaderboard_data = response.json()
            if leaderboard_data:
                df = pd.DataFrame(leaderboard_data)
                
                # Chart 1: Overall performance comparison
                st.subheader("Pipeline Configuration vs. Overall Score")
                st.bar_chart(data=df, x="config_name", y="average_score", color="#6366F1")
                
                st.divider()
                
                # Chart 2: Multidimensional metrics breakdown
                st.subheader("Metric Breakdown by Configuration")
                df_metrics = df.melt(
                    id_vars=["config_name"], 
                    value_vars=["answer_relevancy", "faithfulness", "context_precision", "context_recall"],
                    var_name="RAGAS Metric", 
                    value_name="Score"
                )
                
                import altair as alt
                chart = alt.Chart(df_metrics).mark_bar().encode(
                    x=alt.X('RAGASMetric:N', title=None),
                    y=alt.Y('Score:Q', scale=alt.Scale(domain=[0, 1])),
                    color='RAGAS Metric:N',
                    column=alt.Column('config_name:N', title="Pipeline Configurations")
                ).properties(
                    width=150,
                    height=300
                )
                st.altair_chart(chart, use_container_width=False)
                
            else:
                st.info("Run a benchmark to populate the analytics dashboard.")
        else:
            st.error("Could not load leaderboard data for charting.")
    except Exception as e:
        st.error(f"Connection error: {e}")

# ==========================================
# TAB 4: EXPERIMENT DETAILS & EXPORT
# ==========================================
with tab4:
    st.header("🔍 Past Experiments & CSV Export")
    
    col_list, col_details = st.columns([1, 2])
    
    # Fetch experiments
    try:
        exp_res = requests.get(f"{BACKEND_URL}/experiments/")
        if exp_res.status_code == 200:
            experiments = exp_res.json()
        else:
            experiments = []
            st.error("Failed to load experiments.")
    except Exception as e:
        experiments = []
        st.error(f"Connection error: {e}")
        
    with col_list:
        st.subheader("📚 History")
        if experiments:
            df_exp = pd.DataFrame(experiments)
            # Reorder and format columns
            df_exp_display = df_exp[["id", "name", "status", "created_at"]].sort_values(by="id", ascending=False)
            
            # Select an experiment
            selected_id = st.selectbox(
                "Select Experiment to View Details",
                options=df_exp_display["id"].tolist(),
                format_func=lambda x: f"Experiment #{x} - {df_exp_display[df_exp_display['id'] == x]['name'].values[0]}"
            )
        else:
            st.info("No experiments found.")
            selected_id = None
            
    with col_details:
        if selected_id:
            st.subheader(f"🔍 Experiment #{selected_id} Detailed Results")
            
            try:
                results_res = requests.get(f"{BACKEND_URL}/experiments/{selected_id}/results")
                if results_res.status_code == 200:
                    results_data = results_res.json()
                    
                    if results_data:
                        df_res = pd.DataFrame(results_data)
                        
                        # Display clean tabular layout
                        st.dataframe(
                            df_res[[
                                "config_name", "question", "generated_answer", 
                                "score", "faithfulness", "answer_relevancy", 
                                "context_precision", "context_recall"
                            ]], 
                            use_container_width=True
                        )
                        
                        st.divider()
                        
                        # CSV Export Button
                        csv_data = df_res.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Experiment Results (CSV)",
                            data=csv_data,
                            file_name=f"experiment_{selected_id}_results.csv",
                            mime="text/csv",
                            type="secondary"
                        )
                    else:
                        st.info("No detailed result rows found for this experiment.")
                else:
                    st.error(f"Failed to fetch results: {results_res.text}")
            except Exception as e:
                st.error(f"Error fetching detailed results: {e}")
        else:
            st.info("Select an experiment from the left pane to view details and export.")