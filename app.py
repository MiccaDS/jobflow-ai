import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ====================== CONFIG ======================
st.set_page_config(
    page_title="JobFlow AI - CV Tailor",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 JobFlow AI")
st.subheader("Professional AI CV Tailoring Tool")

# ====================== LOAD API KEY ======================
xai_api_key = os.getenv("XAI_API_KEY")

if not xai_api_key:
    st.error("❌ API key not found!\n\n"
             "Please create a `.env` file in the same folder as app.py with this line:\n"
             "XAI_API_KEY=xai-YourActualKeyHere")
    st.stop()

st.info("✅ API Key loaded from .env | Your data stays private")

# ====================== INPUTS ======================
master_cv = st.text_area(
    "Paste your MASTER CV here",
    height=300,
    placeholder="Paste your full CV text..."
)

job_description = st.text_area(
    "Paste the JOB DESCRIPTION here",
    height=200,
    placeholder="Paste the full job posting..."
)

nice_to_have = st.text_input(
    "Nice to have (optional)",
    placeholder="e.g. Banking experience, German B2, Startup background"
)

# ====================== TAILOR BUTTON ======================
if st.button("✨ Tailor My CV Now", type="primary", use_container_width=True):
    if not master_cv.strip() or not job_description.strip():
        st.warning("Please paste both your Master CV and the Job Description.")
    else:
        with st.spinner("Tailoring your CV with Grok... This may take 10-20 seconds"):
            try:
                prompt = f"""
You are an expert career coach and CV writer.

Master CV:
{master_cv}

Job Description:
{job_description}

Nice to have: {nice_to_have if nice_to_have else "None"}

Task: Rewrite the CV to perfectly match this job.
- Make it concise, achievement-focused, and ATS-friendly.
- Highlight relevant skills and experience.
- Use strong action verbs.
- Keep the tone professional but natural.
- Output ONLY the final tailored CV in clean markdown format.
"""

                response = completion(
                    model="xai/grok-3",
                    messages=[{"role": "user", "content": prompt}],
                    api_key=xai_api_key,
                    temperature=0.7,
                    max_tokens=2000
                )

                tailored_cv = response.choices[0].message.content

                st.success("✅ Here's your tailored CV!")
                st.markdown(tailored_cv)

                st.download_button(
                    label="📥 Download Tailored CV",
                    data=tailored_cv,
                    file_name="Tailored_CV.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.caption("Your data stays private • Powered by Grok + LiteLLM")