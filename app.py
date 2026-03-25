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


st.markdown("""
    <style>
        /* Make the primary button dark/black with nice hover effect */
        div.stButton > button[kind="primary"] {
            background-color: #0f0f0f !important;   /* Very dark black */
            color: #ffffff !important;
            border: 1px solid #444444 !important;
            font-weight: 600;
        }
        
        div.stButton > button[kind="primary"]:hover {
            background-color: #1a1a1a !important;   /* Slightly lighter on hover */
            border-color: #666666 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        /* Optional: make it look even more premium */
        div.stButton > button[kind="primary"] {
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Hide annoying anchor buttons
st.markdown("""
    <style>
        .stApp h1 a, .stApp h2 a, .stApp h3 a, a.anchor-link { display: none !important; }
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

    nice_to_have = st.text_input(
        "Nice to have (optional)", placeholder="e.g. Banking experience, German B2, Startup background",
        value=st.session_state.nice_to_have,
        key="nice_key"
    )
    

    if st.button("✨ Tailor My Job Application Now", type="primary", use_container_width=True):
        if not master_cv.strip() or not job_description.strip():
            st.warning("Please paste both your Master CV and the Job Description.")
        else:
            with st.spinner("Crafting your tailored job application..."):
                try:
                    prompt = f"""Du er en ekspert på norske jobbsøknader og karriererådgivning. 
Skriv en profesjonell, naturlig og målrettet jobbsøknad på **norsk** (bokmål) basert på følgende:

MASTER CV:
{master_cv}

STILLINGSBESKRIVELSE:
{job_description}

Nice to have / ekstra ønsket kompetanse: {nice_to_have if nice_to_have else "Ingen"}

Regler for søknaden:
- Skriv på naturlig, profesjonelt norsk (ikke stivt eller oversatt-engelsk).
- Hold den konsis (ca. 250–400 ord).
- Start med en kort og engasjerende innledning som viser motivasjon for akkurat denne stillingen.
- Trekk frem 3–4 mest relevante erfaringer/kompetanser og koble dem direkte til kravene i stillingsannonsen.
- Bruk konkrete resultater og handlingsverb (utviklet, økte, bidro til, ledet osv.).
- Avslutt med hvorfor du passer godt og at du gjerne tar en prat.
- Bruk "jeg" og skriv i første person.
- Ingen overskrifter, ingen markdown, ingen bullet points, ingen forklaringer. Bare ren søknadstekst.
- Tilpass tonen til en norsk arbeidsgiver: direkte, ydmyk, samarbeidsorientert og positiv.

Skriv nå den ferdige søknaden:
"""

                    response = completion(
                        model="huggingface/meta-llama/Llama-3.1-8B-Instruct",   # eller normistral-7b-warm-instruct
                        messages=[{"role": "user", "content": prompt}],
                        api_key=HUGGINGFACE_API_KEY,
                        temperature=0.6,      # 0.5–0.7 er best for jobbsøknader
                        max_tokens=1800,
                        top_p=0.95
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

# History 
with st.sidebar:
    if st.session_state.history:
        st.caption(f"{len(st.session_state.history)} previous applications saved")

