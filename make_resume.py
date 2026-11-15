# make_resume.py — generates a 1-page ATS-friendly resume PDF
import re, os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

W, H = 210, 297; M = 15
NAVY=(22,50,79); LINK=(11,83,148); DARK=(34,34,34); GRAY=(70,70,70)
TOKEN = re.compile(r'(\*\*.+?\*\*|\[.+?\]\(.+?\))')

GITHUB="github.com/darshaks-debug"; REPO="github.com/darshaks-debug/python-foundations"
LINKEDIN="linkedin.com/in/s-darshak-807079449"; PORTFOLIO="darshak-portfolio.streamlit.app"
EXPENSE="darshak-expense-tracker.streamlit.app"; API="python-foundations-production.up.railway.app/docs"
RAG="darshak-rag-pdf.streamlit.app"; ANALYZER="darshak-resume-analyzer.streamlit.app"
CREDLY="credly.com/users/senthilkumar-darshak"; EMAIL="sdarshak70@gmail.com"
def lk(d,t=None): return f"[{t or d}](https://{d})"

def build(path, lh, body, gap, meta):
    pdf = FPDF(format="A4"); pdf.core_fonts_encoding = "windows-1252"
    pdf.set_margins(M, 12, M); pdf.set_auto_page_break(True, margin=12)
    pdf.set_title("Senthilkumar Darshak — Resume"); pdf.set_author("Senthilkumar Darshak")
    pdf.add_page()

    def rich(text, size=None, color=DARK, indent=0, bullet=False):
        size = size or body
        pdf.set_font("Helvetica","",size); pdf.set_text_color(*color)
        pdf.set_left_margin(M+indent); pdf.set_x(M if bullet else M+indent)
        if bullet: pdf.write(lh, "•  ")
        for tok in TOKEN.split(text):
            if not tok: continue
            if tok.startswith("**"):
                pdf.set_font("Helvetica","B",size); pdf.write(lh, tok[2:-2]); pdf.set_font("Helvetica","",size)
            elif tok.startswith("["):
                m = re.match(r'\[(.+?)\]\((.+?)\)', tok); t,u = m.groups()
                pdf.set_text_color(*LINK); pdf.write(lh, t, link=u); pdf.set_text_color(*color)
            else: pdf.write(lh, tok)
        pdf.ln(lh); pdf.set_left_margin(M)

    def section(t):
        pdf.ln(gap); pdf.set_font("Helvetica","B",10.5); pdf.set_text_color(*NAVY)
        pdf.cell(0,5,t,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
        y=pdf.get_y()+0.5; pdf.set_draw_color(*NAVY); pdf.set_line_width(0.25); pdf.line(M,y,W-M,y); pdf.ln(2.0)

    def center_line(parts, size=9, h=4.4):
        pdf.set_font("Helvetica","",size)
        ws=[pdf.get_string_width(t) for t,_,_ in parts]
        pdf.set_xy((W-sum(ws))/2, pdf.get_y())
        for (t,u,c),w in zip(parts,ws):
            pdf.set_text_color(*c); pdf.cell(w,h,t,link=u or "",new_x=XPos.RIGHT,new_y=YPos.TOP)
        pdf.ln(h+0.4)

    pdf.set_font("Helvetica","B",17); pdf.set_text_color(*NAVY)
    pdf.cell(0,8,"SENTHILKUMAR DARSHAK",align="C",new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    pdf.set_font("Helvetica","B",10.3); pdf.set_text_color(*DARK)
    pdf.cell(0,5.5,"Python Backend Developer  |  AI Application Developer",align="C",new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    pdf.ln(0.8)
    center_line([("Coimbatore, India (open to relocation)  ·  +91 88254 29280  ·  ",None,DARK),(EMAIL,"mailto:"+EMAIL,LINK)])
    center_line([(GITHUB,"https://"+GITHUB,LINK),("  ·  ",None,DARK),(LINKEDIN,"https://"+LINKEDIN,LINK),("  ·  ",None,DARK),(PORTFOLIO,"https://"+PORTFOLIO,LINK)])

    section("SUMMARY")
    rich("MCA graduate specializing in Python backend and AI application development. Built and deployed three live applications featuring JWT authentication, PostgreSQL with versioned migrations, automated testing with CI/CD, and a from-scratch RAG pipeline with page-level citations. Seeking an entry-level Python backend / full-stack / AI application developer role.")

    section("TECHNICAL SKILLS")
    rich("**Languages:** Python, SQL")
    rich("**Backend & Databases:** FastAPI, REST APIs, SQLAlchemy, Alembic, Pydantic, PostgreSQL, SQLite, JWT authentication, Argon2 password hashing")
    rich("**AI / LLM Engineering:** RAG pipelines, ChromaDB, vector embeddings (SentenceTransformers), Google Gemini API, prompt engineering, structured JSON output")
    rich("**DevOps & Testing:** Docker, GitHub Actions (CI/CD), Pytest, Git/GitHub, Railway, Streamlit Cloud, Streamlit")

    section("PROJECTS — DEPLOYED & LIVE (2026)")
    rich(f"Source for all projects: {lk(REPO)}  ·  public daily build log: PROGRESS.md", size=meta, color=GRAY)

    pdf.set_font("Helvetica","B",10); pdf.set_text_color(*DARK)
    pdf.cell(0,lh+0.8,"AI Expense Tracker — Secure Full-Stack Application",new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    rich(f"**Live:** {lk(EXPENSE)}  ·  **API:** {lk(API)}", size=meta, color=GRAY)
    rich("**Stack:** FastAPI, PostgreSQL, Alembic, JWT, Docker, GitHub Actions, Gemini", size=meta, color=GRAY)
    rich("Built a multi-user REST API with JWT authentication and Argon2 hashing; enforced per-user data isolation at the query level, verified by automated tests.", indent=3.2, bullet=True)
    rich("Managed PostgreSQL schema with Alembic migrations run automatically on deploy; containerized with Docker; 7-test Pytest suite gated by GitHub Actions CI on every push.", indent=3.2, bullet=True)
    rich("Integrated Gemini for automatic expense categorization and spending analysis with graceful fallback on API failure.", indent=3.2, bullet=True)

    pdf.ln(0.8); pdf.set_font("Helvetica","B",10); pdf.set_text_color(*DARK)
    pdf.cell(0,lh+0.8,"Chat with your PDF — RAG Application (built from scratch, no framework)",new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    rich(f"**Live:** {lk(RAG)}", size=meta, color=GRAY)
    rich("**Stack:** Python, ChromaDB, SentenceTransformers, Gemini, Streamlit", size=meta, color=GRAY)
    rich("Engineered the full RAG pipeline without frameworks: PDF extraction, overlapping chunking, local embeddings, vector retrieval, and grounded answers with page-level citations.", indent=3.2, bullet=True)
    rich("Implemented per-user document isolation via session-scoped ChromaDB collections to prevent cross-user data leakage.", indent=3.2, bullet=True)
    rich('Added exponential-backoff retries for rate limits/server errors and an explicit "not in document" fallback to curb hallucinations.', indent=3.2, bullet=True)

    pdf.ln(0.8); pdf.set_font("Helvetica","B",10); pdf.set_text_color(*DARK)
    pdf.cell(0,lh+0.8,"AI Resume Analyzer — Structured LLM Output",new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    rich(f"**Live:** {lk(ANALYZER)}", size=meta, color=GRAY)
    rich("**Stack:** Python, Gemini, pypdf, Streamlit", size=meta, color=GRAY)
    rich("Built a resume-to-job-description matcher returning a match score, missing skills, and rewrite suggestions as strict JSON, rendered in a dynamic UI.", indent=3.2, bullet=True)
    rich("Handled real-world edge cases: scanned/empty PDFs, markdown-wrapped JSON, and malformed model output.", indent=3.2, bullet=True)

    section("EXPERIENCE")
    rich("**Career Break & Professional Development**  |  2022 – 2026")
    rich("Personal career break; completed a full-time backend/AI engineering intensive in 2026, shipping the deployed applications above (public daily build log on GitHub).", indent=3.2, bullet=True)
    rich("**Data Science Intern** — Institute of Electronics & Telecommunication Engineers (IETE), Coimbatore  |  May 2022 – Jun 2022")
    rich("Built a Twitter sentiment analysis project using the Twitter Streaming API, NLTK, pandas, and an SVC classifier.", indent=3.2, bullet=True)

    section("EDUCATION")
    rich("**Master of Computer Applications (MCA)** — Bharathiar University, Coimbatore  |  2020 – 2022  |  CGPA 8.26")
    rich("MCA project: Optical Character Recognition system (Tesseract, LSTM)", size=body-0.4, color=GRAY)
    rich("**Bachelor of Computer Applications (BCA)** — V L B Janakiammal College of Arts and Science  |  2017 – 2020  |  CGPA 7.42")

    section("CERTIFICATION")
    rich(f"**Google Cybersecurity Certificate** — Coursera (8-course program)  ·  Credential: {lk(CREDLY)}")

    pages = pdf.page
    pdf.output(path)
    return pages

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "Senthilkumar_Darshak_Resume_2026.pdf")
    for cfg in [(4.2,9.1,1.5,8.4),(4.0,8.9,1.2,8.2)]:
        if build(path, *cfg) == 1: break
    print("✅ Saved:", os.path.abspath(path))