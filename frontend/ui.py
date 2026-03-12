import streamlit as st

import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.skill_extractor import extract_skills
from utils.question_generator import generate_questions
from utils.answer_generator import generate_answer
from utils.resume_parser import extract_text_from_pdf
from utils.ats_score import calculate_ats_score
from utils.resume_improver import improve_resume
st.set_page_config(page_title="AI Interview Preparation App")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title("AI Interview Preparation System")

# Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# Job Description
job_description = st.text_area("Paste Job Description")

resume_text = ""
skills_text = ""

# Session State Initialization
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []

if "hr_questions" not in st.session_state:
    st.session_state.hr_questions = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

# Extract Resume Data
# Extract Resume Data
if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    if job_description:

        st.subheader("Extracted Skills")

        skills = extract_skills(resume_text, job_description)

        skills_text = ", ".join(skills)

        st.write(skills)
    # ATS Score
    if job_description:

        score, matched = calculate_ats_score(job_description, resume_text)

        st.subheader("ATS Score")

        st.write(f"Your ATS Score: {score}%")

        st.subheader("Matched Skills")

        st.write(matched)

st.subheader("Resume Improvement")

if st.button("Improve My Resume"):

    with st.spinner("Improving your resume..."):

        improved_resume = improve_resume(resume_text, job_description)

        st.write(improved_resume)
# Generate Questions
if uploaded_file is not None and job_description:

    if st.button("Generate Interview Questions"):

        with st.spinner("Generating questions..."):

            st.session_state.tech_questions = generate_questions(
                job_description,
                resume_text,
                skills_text,
                10,
                question_type="Technical"
            )

            st.session_state.hr_questions = generate_questions(
                job_description,
                resume_text,
                skills_text,
                5,
                question_type="HR"
            )


    # Generate More Questions
    if st.session_state.tech_questions:

        if st.button("Generate More Questions"):

            with st.spinner("Generating more questions..."):

                more_tech = generate_questions(
                    job_description,
                    resume_text,
                    skills_text,
                    5,
                    question_type="Technical"
                )

                more_hr = generate_questions(
                    job_description,
                    resume_text,
                    skills_text,
                    3,
                    question_type="HR"
                )

                st.session_state.tech_questions.extend(more_tech)
                st.session_state.hr_questions.extend(more_hr)


# Display Technical Questions
if st.session_state.tech_questions:

    st.subheader("Technical Interview Questions")

    for i, q in enumerate(st.session_state.tech_questions):

        st.write(f"{i+1}. {q}")

        if st.button("Generate Answer", key=f"tech_btn_{i}"):

            ans = generate_answer(q)

            st.session_state.answers[f"tech_{i}"] = ans

        if f"tech_{i}" in st.session_state.answers:

            st.write(st.session_state.answers[f"tech_{i}"])

        st.divider()


# Display HR Questions
if st.session_state.hr_questions:

    st.subheader("HR Interview Questions")

    for i, q in enumerate(st.session_state.hr_questions):

        st.write(f"{i+1}. {q}")

        if st.button("Generate Answer", key=f"hr_btn_{i}"):

            ans = generate_answer(q)

            st.session_state.answers[f"hr_{i}"] = ans

        if f"hr_{i}" in st.session_state.answers:

            st.write(st.session_state.answers[f"hr_{i}"])

        st.divider()