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

# Custom styling
st.markdown("""
    <style>
        div.stButton > button[kind="primary"] {
            background-color: #0f0f0f !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #1a1a1a !important;
            border-color: #666666 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        .stApp h1 a, .stApp h2 a, .stApp h3 a, a.anchor-link { 
            display: none !important; 
        }
    </style>
""", unsafe_allow_html=True)

st.subheader("The Job Application Optimizer")

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    st.error("❌ Hugging Face API key not found!")
    st.stop()

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

# Sidebar
with st.sidebar:
    st.title("🚀 JobFlow AI")
    tool = st.radio("Select Tool:", ["Job Application Tailor", "Cv Enhancer", "Interview Prep"])
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

# ====================== JOB APPLICATION TAILOR ======================
if tool == "Job Application Tailor":
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        master_cv = st.text_area(
            "Paste your MASTER CV here",
            placeholder="Paste your full CV text...",
            height=380,
            value=st.session_state.master_cv,
            key="master_cv_key"
        )
    with col2:
        job_description = st.text_area(
            "Paste the JOB DESCRIPTION here",
            placeholder="Paste the full job posting...",
            height=380,
            value=st.session_state.job_desc,
            key="job_desc_key"
        )

    # Språkvalg + Nice to have
    col_lang, col_nice = st.columns([1, 2])
    with col_lang:
        language = st.selectbox(
            "Language for the application",
            options=["Norsk (bokmål)", "English"],
            index=0,  # Default = Norsk
            key="language_key"
        )
    
    with col_nice:
        nice_to_have = st.text_input(
            "Nice to have (optional)",
            placeholder="e.g. Banking experience, German B2, Startup background",
            value=st.session_state.nice_to_have,
            key="nice_key"
        )

    # Generate button
    if st.button("✨ Tailor My Job Application Now", type="primary", use_container_width=True):
        if not master_cv.strip() or not job_description.strip():
            st.warning("Please paste both your Master CV and the Job Description.")
        else:
            with st.spinner("Crafting your tailored job application..."):
                try:
                    if language == "Norsk (bokmål)":
                        prompt = f"""Du er en ekspert på norske jobbsøknader og karriererådgivning.
Skriv en profesjonell, naturlig og målrettet jobbsøknad på **norsk bokmål** basert på dette:

MASTER CV:
{master_cv}

STILLINGSBESKRIVELSE:
{job_description}

Nice to have: {nice_to_have if nice_to_have else "Ingen"}

Regler du MÅ følge:
- Naturlig og flytende norsk (ikke stivt eller oversatt-engelsk).
- Lengde ca. 300–500 ord.
- Start med en kort, engasjerende innledning som viser hvorfor du søker akkurat denne stillingen.
- Trekk frem de mest relevante erfaringene og koble dem direkte til kravene i annonsen.
- Bruk konkrete resultater og sterke handlingsverb (bidro til, utviklet, økte, ledet osv.).
- Avslutt positivt med "vennlig hilsen, [navn] og hvorfor du passer godt for stillingen og at du gjerne tar en prat.
- Skriv i første person ("jeg").
- Kun ren tekst – ingen overskrifter, ingen markdown, ingen bullet points, ingen forklaringer.

Skriv nå den ferdige søknaden:
"""
                    else:  # English
                        prompt = f"""You are an expert career coach and job application specialist.
Write a professional, natural and targeted job application in **English** based on this:

MASTER CV:
{master_cv}

JOB DESCRIPTION:
{job_description}

Nice to have: {nice_to_have if nice_to_have else "None"}

Rules you MUST follow:
- Natural, professional and fluent English.
- Length approx. 300-500 words.
- Start with a short, engaging introduction showing why you are applying for this specific position.
- Highlight 3–4 most relevant experiences and link them directly to the requirements in the job ad.
- Use concrete achievements and strong action verbs.
- End positively with why you are a good fit and that you would welcome a conversation.
- Write in first person ("I").
- Only clean text – no headings, no markdown, no bullet points, no explanations.

Write the final job application now:
"""

                    response = completion(
                        model="huggingface/meta-llama/Llama-3.1-8B-Instruct",
                        messages=[{"role": "user", "content": prompt}],
                        api_key=HUGGINGFACE_API_KEY,
                        temperature=0.6,
                        max_tokens=1800,
                        top_p=0.95
                    )
                    
                    result = response.choices[0].message.content.strip()
                    
                    st.success(f"✅ Your tailored {'norske' if language == 'Norsk (bokmål)' else 'English'} application is ready!")
                    st.markdown(result)
                    
                    file_name = f"Tailored_Application_{'NO' if language == 'Norsk (bokmål)' else 'EN'}.txt"
                    st.download_button(
                        label="📥 Download Application",
                        data=result,
                        file_name=file_name,
                        mime="text/plain"
                    )
                    
                    # Save to history
                    st.session_state.history.append({
                        "title": f"Application for: {job_description[:60]}... ({'NO' if language == 'Norsk (bokmål)' else 'EN'})",
                        "master_cv": master_cv,
                        "job_desc": job_description,
                        "nice_to_have": nice_to_have,
                        "result": result,
                        "language": language
                    })

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Show previous result if selected from sidebar
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

# Footer info in sidebar
with st.sidebar:
    if st.session_state.history:
        st.caption(f"{len(st.session_state.history)} previous applications saved")
