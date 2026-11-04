import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Darshak's Portfolio", page_icon="💻", layout="wide")

# 2. Custom CSS to make it look clean
st.markdown("""
    <style>
    .big-font { font-size:50px !important; font-weight: bold; }
    .sub-font { font-size:20px !important; color: gray; }
    .project-card { 
        background-color: #1E1E1E; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<p class="big-font">Hi, I\'m Darshak 👋</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">AI Full-Stack Developer | Python | FastAPI | Streamlit | LLMs</p>', unsafe_allow_html=True)
st.write("I build intelligent web applications that solve real-world problems. Recently, I've been focused on building end-to-end RAG pipelines and AI-powered tools.")
st.write("---")

# 4. Skills Section
st.subheader("🛠️ Technical Skills")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Backend**")
    st.write("- Python, FastAPI, Uvicorn")
    st.write("- SQLAlchemy, SQLite, PostgreSQL")
    st.write("- Docker")

with col2:
    st.markdown("**AI & Data**")
    st.write("- Google Gemini API")
    st.write("- ChromaDB, Vector Embeddings")
    st.write("- RAG (Retrieval-Augmented Generation)")

with col3:
    st.markdown("**Frontend & Cloud**")
    st.write("- Streamlit, HTML/CSS")
    st.write("- Vercel, Streamlit Cloud")
    st.write("- Git, GitHub Actions")

st.write("---")

# 5. Projects Section
st.subheader("🚀 Featured Projects")

# Project 1: AI Resume Analyzer
st.markdown("""
<div class="project-card">
    <h3>📄 AI Resume Analyzer</h3>
    <p>A tool that compares a resume against a job description using Gemini LLM. It extracts text from PDFs, analyzes the match, identifies missing skills, and provides actionable resume tips.</p>
    <p><b>Stack:</b> Streamlit, Google Gemini, PyPDF</p>
</div>
""", unsafe_allow_html=True)
# Replace the URLs below with your actual live links!
st.link_button("🔴 Live Demo", "https://python-foundations-4kev8dkppbgp28dhoqujss.streamlit.app")
st.link_button("💻 Source Code", "https://github.com/darshaks-debug/python-foundations/blob/main/resume_analyzer.py")

# Project 2: Chat with your PDF (RAG)
st.markdown("""
<div class="project-card">
    <h3>🧠 Chat with your PDF (RAG Pipeline)</h3>
    <p>A custom-built Retrieval-Augmented Generation (RAG) app. Upload any PDF and chat with it. The app chunks text with overlap, creates vector embeddings, stores them in ChromaDB, and uses Gemini to answer questions with page citations.</p>
    <p><b>Stack:</b> Streamlit, ChromaDB, SentenceTransformers, Gemini</p>
</div>
""", unsafe_allow_html=True)
st.link_button("🔴 Live Demo", "https://python-foundations-kps7bv6epcpdzpnjntzcpn.streamlit.app")
st.link_button("💻 Source Code", "https://github.com/darshaks-debug/python-foundations/blob/main/rag_app.py")

# Project 3: AI Expense Tracker
st.markdown("""
<div class="project-card">
    <h3>💰 AI Expense Tracker</h3>
    <p>A full-stack CRUD application. The backend is a FastAPI REST API deployed on Vercel. The frontend allows users to track expenses, which are automatically categorized by AI (e.g., "McDonalds" -> "Food").</p>
    <p><b>Stack:</b> FastAPI, SQLAlchemy, Streamlit, Docker, Vercel</p>
</div>
""", unsafe_allow_html=True)
st.link_button("🔴 Live Demo", "https://python-foundations-abwdzzq9nbxbjyvudpdp6s.streamlit.app")
st.link_button("💻 Source Code", "https://github.com/darshaks-debug/python-foundations")

st.write("---")

# 6. Contact Section
st.subheader("📫 Let's Connect")
st.write("I am actively looking for entry-level AI/Backend Developer roles. Feel free to reach out!")
st.markdown("[LinkedIn](https://www.linkedin.com/in/s-darshak-807079449/) | [GitHub](https://github.com/darshaks-debug) | [Email](mailto:sdarshak70@gmail.com)")