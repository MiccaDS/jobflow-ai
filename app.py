import streamlit as st
from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()  # loads your secret key from .env

st.set_page_config(page_title="JobFlow AI", page_icon="🚀", layout="wide")
st.title("🚀 JobFlow AI")
st.subheader("Professional AI CV Tailoring Tool")
st.caption("Your data stays private • Built for real job hunters")

# Input fields
master_cv = st.text_area("Paste your MASTER CV here", height=350, placeholder="Full CV text...")
job_desc = st.text_area("Paste the JOB DESCRIPTION here", height=250, placeholder="Full job posting...")

if st.button("✨ Tailor My CV Now", type="primary", use_container_width=True):
    if master_cv.strip() and job_desc.strip():
        with st.spinner("AI is working... (10-30 seconds)"):
            try:
                response = completion(
                    model="xai/grok-4-1-fast-reasoning",   # ← You can change to "xai/grok-4.20-reasoning" if you want
                    messages=[{"role": "user", "content": f"""You are an expert resume writer. 
                    Tailor the CV to perfectly match the job. 
                    Keep the original achievements and the candidate's natural tone. 
                    Make every bullet relevant and strong. Naturally include important keywords from the job.

                    MASTER CV:
                    {master_cv}

                    JOB DESCRIPTION:
                    {job_desc}"""}]
                )
                tailored = response.choices[0].message.content
                
                st.success("✅ Your professionally tailored CV is ready!")
                st.markdown(tailored)
                
                # Fixed download button
                st.download_button(
                    label="📥 Download Tailored CV",
                    data=tailored,
                    file_name="tailored_cv.txt",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please paste both your CV and the job description")