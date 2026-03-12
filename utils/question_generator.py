import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st


client = Groq(api_key=st.secrets["GROQ_API_KEY"])
load_dotenv()




def generate_questions(job_description, resume_text, skills_text, num_questions, question_type):

    prompt = f"""
Generate {num_questions} {question_type} interview questions.

The questions should progress from:
Beginner level → Intermediate level → Advanced level.

Base the questions on the following information.

Resume:
{resume_text}

Job Description:
{job_description}

Skills:
{skills_text}

Return ONLY the questions.
Do NOT include explanations.
Do NOT include question numbers.
Do NOT include headings like "Here are the questions".
Do NOT include any text other than the questions themselves.
Do NOT include any formatting like bullet points or numbering.
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.4,
        max_tokens=800
    )

    result = response.choices[0].message.content

    questions = result.split("\n")

    questions = [q.strip() for q in questions if q.strip()]

    return questions