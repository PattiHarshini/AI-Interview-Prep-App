import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def calculate_ats_score(job_description, resume_text):

    prompt = f"""
You are an ATS system.

Compare the resume with the job description.

Return results in this exact format:

ATS Score: <number between 0 and 100>
Matched Skills: <comma separated skills>

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.3,
        max_tokens=200
    )

    result = response.choices[0].message.content

    # Extract ATS Score
    score_match = re.search(r'ATS Score:\s*(\d+)', result)

    if score_match:
        score = int(score_match.group(1))
    else:
        score = 0

    # Extract matched skills
    skills_match = re.search(r'Matched Skills:\s*(.*)', result)

    if skills_match:
        matched_skills = skills_match.group(1)
    else:
        matched_skills = "Not detected"

    return score, matched_skills