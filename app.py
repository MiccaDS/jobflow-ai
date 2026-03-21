import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os

#api han enkelt erstattes med en annen som x ai
# Load environment variables from .env file
load_dotenv()

# ====================== CONFIG ======================
st.set_page_config(
    page_title="JobFlow AI - Job Application Tailor",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 JobFlow AI")
st.subheader("Professional AI Job Application Tailoring Tool")

# ====================== LOAD API KEY ======================
#XAI_API_KEY
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    st.error("❌ API key not found!\n\n"
             "Please create a `.env` file in the same folder as app.py with this line:\n"
             "HUGGINGFACE_API_KEY=hf_YourActualKeyHere")
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
        with st.spinner("Tailoring your application with huggingface... This may take 10-20 seconds"):
            try:
                prompt = f"""
You are an expert career coach and Job application specialist.

Master CV:
{master_cv}

Job Description:
{job_description}

Nice to have: {nice_to_have if nice_to_have else "None"}

Task: Write a job application using the Master CV and Job Descriptionto perfectly match this job.
- Make it concise, achievement-focused, and ATS-friendly.
- Include relevant skills and experience that are given in the Master CV.
- Use strong action verbs.
- Keep the tone professional but natural.
- Output ONLY the final tailored application in a clean professional format, no need for multiple titles or markdown-formatting.
"""

                response = completion(
                    #"xai/grok-3"
                    model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    api_key=HUGGINGFACE_API_KEY,
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
st.caption("Your data stays private • Powered by Huggingface + LiteLLM")