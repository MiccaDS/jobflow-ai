import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="JobFlow AI - Job Application Tailor",
    page_icon="🚀",
    layout="wide"
)

# Hide annoying anchor buttons
st.markdown("""
    <style>
        .stApp h1 a, .stApp h2 a, .stApp h3 a, a.anchor-link { display: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 JobFlow AI")
st.subheader("Professional AI Job Application Tailoring Tool")

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    st.error("❌ Hugging Face API key not found!")
    st.stop()

#st.info("✅ API Key loaded | Your data stays private")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "master_cv" not in st.session_state:
    st.session_state.master_cv = ""
if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""
if "nice_to_have" not in st.session_state:
    st.session_state.nice_to_have = ""
if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

# ====================== SIDEBAR ======================
with st.sidebar:
    st.title("🚀 Tools")
    tool = st.radio("Select Tool:", ["Job Application Tailor", "Cover Letter Writer", "Interview Prep", "Job Analysis"])

    st.divider()
    if st.session_state.history:
        st.subheader("Recent Applications")
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(item["title"], key=f"load_{i}"):
                st.session_state.master_cv = item["master_cv"]
                st.session_state.job_desc = item["job_desc"]
                st.session_state.nice_to_have = item["nice_to_have"]
                st.session_state.selected_result = item["result"]
                st.rerun()

# ====================== MAIN AREA ======================
if tool == "Job Application Tailor":
    st.header("✨ Tailor My Job Application")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        master_cv = st.text_area(
            "Paste your MASTER CV here",
            height=380,
            value=st.session_state.master_cv,
            key="master_cv_key"
        )

    with col2:
        job_description = st.text_area(
            "Paste the JOB DESCRIPTION here",
            height=380,
            value=st.session_state.job_desc,
            key="job_desc_key"
        )

    nice_to_have = st.text_input(
        "Nice to have (optional)",
        value=st.session_state.nice_to_have,
        key="nice_key"
    )

    if st.button("✨ Tailor My Job Application Now", type="primary", use_container_width=True):
        if not master_cv.strip() or not job_description.strip():
            st.warning("Please paste both your Master CV and the Job Description.")
        else:
            with st.spinner("Crafting your tailored job application..."):
                try:
                    prompt = f"""
You are an expert career coach and job application specialist.

Master CV:
{master_cv}

Job Description:
{job_description}

Nice to have: {nice_to_have if nice_to_have else "None"}

Task: Write a complete, professional job application.
- Make it concise, targeted and achievement-focused
- Highlight relevant skills from the Master CV
- Use strong action verbs
- Keep tone professional but natural
- Output ONLY the final job application text.
"""

                    response = completion(
                        model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
                        messages=[{"role": "user", "content": prompt}],
                        api_key=HUGGINGFACE_API_KEY,
                        temperature=0.7,
                        max_tokens=2200
                    )

                    result = response.choices[0].message.content

                    st.success("✅ Your Tailored Job Application is Ready!")
                    st.markdown(result)

                    st.download_button(
                        label="📥 Download Application",
                        data=result,
                        file_name="Tailored_Job_Application.txt",
                        mime="text/plain"
                    )

                    # Save to history
                    st.session_state.history.append({
                        "title": f"Application for: {job_description[:60]}...",
                        "master_cv": master_cv,
                        "job_desc": job_description,
                        "nice_to_have": nice_to_have,
                        "result": result
                    })

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Show previous result if selected
    if st.session_state.selected_result:
        st.divider()
        st.header("📄 Previous Application")
        st.markdown(st.session_state.selected_result)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Close Preview"):
                st.session_state.selected_result = None
                st.rerun()
        with col2:
            st.download_button(
                "📥 Download This Version",
                st.session_state.selected_result,
                file_name="Previous_Application.txt",
                mime="text/plain"
            )

else:
    st.header(tool)
    st.info(f"{tool} is coming soon...")

# History count
with st.sidebar:
    if st.session_state.history:
        st.caption(f"{len(st.session_state.history)} previous applications saved")