import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import json

# 1. Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Define the AI Function (Must be defined BEFORE it is called)
def analyze_match(resume_text, job_description):
    prompt = f"""
    You are an expert tech recruiter. I will provide a Resume and a Job Description.
    Analyze the match and return your evaluation strictly as a JSON object.
    Do not include any markdown formatting like ```json or ```. Just return the raw JSON string.

    The JSON must have exactly this structure:
    {{
        "match_score": <integer from 0 to 100>,
        "missing_skills": [<list of 3 to 5 strings of crucial skills missing from the resume>],
        "resume_tips": [<list of 3 specific bullet points to improve the resume for this specific job>],
        "summary": "<A 2-sentence summary of why they are a good or bad fit>"
    }}

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """

    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(prompt)
        
        # Clean the response just in case the AI adds markdown
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        
        # Parse the string into a Python dictionary
        data = json.loads(clean_json)
        
        # Display the results beautifully
        st.divider()
        st.subheader("Analysis Results")
        
        # The Score
        score_color = "green" if data["match_score"] > 70 else "orange" if data["match_score"] > 50 else "red"
        st.markdown(f"### Match Score: :{score_color}[{data['match_score']}%]")
        st.write(f"*{data['summary']}*")
        
        # Two columns for Skills and Tips
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.error("⚠️ Missing Skills")
            for skill in data["missing_skills"]:
                st.write(f"- {skill}")
                
        with res_col2:
            st.success("💡 Resume Tips")
            for tip in data["resume_tips"]:
                st.write(f"- {tip}")
                
    except Exception as e:
        st.error(f"An error occurred: {e}")

# 3. Setup the Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and paste a job description to see how well you match!")

# Create two columns for side-by-side inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.subheader("2. Paste Job Description")
    job_description = st.text_area("Paste the JD here...", height=250)

# 4. The Analyze Button
if st.button("Analyze Match", type="primary"):
    if uploaded_file is None or not job_description.strip():
        st.warning("Please upload a resume AND paste a job description.")
    else:
        with st.spinner("Extracting text from PDF..."):
            reader = PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"
        
        # --- NEW CHECK HERE ---
        if len(resume_text.strip()) == 0:
            st.error("Could not extract text from this PDF. It might be a scanned image. Please try a different PDF (e.g., export your resume as a text-based PDF).")
        else:
            with st.spinner("AI is analyzing your match..."):
                analyze_match(resume_text, job_description)