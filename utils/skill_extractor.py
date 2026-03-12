import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_skills(resume_text, job_description):

    prompt = f"""
Extract all technical skills from the following resume and job description.

Return only a clean comma-separated list of skills.

Resume:
{resume_text}

Job Description:
{job_description}

Rules:
- Extract programming languages, frameworks, tools, databases, and technologies.
- Do NOT include explanations.
- Return only the skills list.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200
    )

    skills_text = response.choices[0].message.content

    skills = [s.strip() for s in skills_text.split(",") if s.strip()]

    return list(set(skills))