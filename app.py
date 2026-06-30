import streamlit as st
import pdfplumber
import ollama
import re

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 80px !important;
    font-weight: 900 !important;
    color: #00FFFF ;
    text-shadow: 0 0 25px rgba(0,255,255,0.7);
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    font-size: 24px;
    color: #b0b0b0 !important;
    margin-top: 0px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">AI Resume Analyzer</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Optimize your resume for ATS systems, recruiter readability, and job matching.</p>',
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    st.markdown("# Resume copilot")
    st.divider()
    st.markdown("""
    ### Features
    ✔ General Resume Review  
    ✔ ATS Score Analysis  
    ✔ Job Matching  
    ✔ Resume Improvements  
    """)
    st.divider()
    st.markdown("""
    ### Tech Stack
    - Streamlit
    - Llama3
    - PDFPlumber
    """)
    st.divider()
    st.caption("Built by Atharva")

uploaded_file = st.file_uploader("Upload Resume (Security Guarenteed)", type="pdf")

job_description = st.text_area("Paste Job Description (required for ATS analysis)")

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    with st.expander("View Extracted Resume Text"):
        st.write(text[:3000])

    col1, col2 = st.columns(2)

    with col1:
        general_clicked = st.button("General Review")

    if general_clicked:
        prompt = f"""
        Review this resume professionally.

        Focus on:
        - clarity
        - structure
        - wording
        - project quality
        - bullet point strength
        - professionalism

        Give:
        1. Overall Review
        2. Major Problems
        3. What Is Done Well
        4. Exact Improvements
        5. Better Resume Bullet Examples

        Job Description:
        {job_description}

        Resume:
        {text}
        """

        progress = st.progress(0)

        status = st.empty()

        status.text("Reading resume...")
        progress.progress(20)

        status.text("Evaluating resume structure...")
        progress.progress(40)

        status.text("Analyzing wording and clarity...")
        progress.progress(60)

        status.text("Generating improvement suggestions...")
        progress.progress(80)

        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])

        progress.progress(100)
        status.text("Review complete.")
        st.subheader("General Resume Review")
        response_text = response['message']['content']
        st.markdown(response_text)

    with col2:
        ats_clicked = st.button("ATS Analysis")

    if ats_clicked:

        if not job_description:
            st.warning("Please paste a job description.")

        else:
            prompt = f"""
            You are an expert ATS resume evaluator.
            Analyze this resume and provide:

            1. ATS Score out of 100
            2. Match Percentage
            3. Missing Keywords
            4. ATS Compatibility Problems
            5. Formatting Issues
            6. Skills Missing
            7. Improvements Needed

            IMPORTANT:
            Start your response EXACTLY like this:

            ATS Score: <number>/100

            Job Description:
            {job_description}
            
            Resume:
            {text}
            """

            progress = st.progress(0)

            status = st.empty()

            status.text("Reading resume...")
            progress.progress(20)

            status.text("Analyzing ATS compatibility...")
            progress.progress(40)

            status.text("Matching with job description...")
            progress.progress(60)

            status.text("Generating recommendations...")
            progress.progress(80)

            response = ollama.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}])

            progress.progress(100)
            status.text("Analysis complete.")
            st.subheader("ATS Analysis")
            response_text = response['message']['content']
            match = re.search(r'ATS Score:\s*(\d+)', response_text)

            if match:
                score = int(match.group(1))
                st.metric("ATS Score", f"{score}/100")

            st.markdown(response_text)

st.divider()

st.subheader("Resume Bullet Rewriter")

bullet_input = st.text_area(
    "Paste a weak resume bullet point"
)

if st.button("Rewrite Bullet Point"):

    rewrite_prompt = f"""
    Rewrite this resume bullet professionally.

    Make it:
    - concise
    - impactful
    - ATS-friendly
    - achievement-oriented

    Bullet Point:
    {bullet_input}
    """

    with st.spinner("Rewriting bullet point..."):

        rewrite_response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'user',
                    'content': rewrite_prompt
                }
            ]
        )

        st.success("Improved Resume Bullet")

        st.markdown(
            rewrite_response['message']['content']
        )