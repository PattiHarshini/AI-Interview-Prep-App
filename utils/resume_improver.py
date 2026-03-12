import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def improve_resume(resume_text, job_description):

    prompt = f"""
You are a professional resume reviewer.

Improve the candidate's resume based on the job description.

Provide:

1. Improved resume summary
2. Suggested bullet points for experience
3. Skills to add
4. General improvement tips

Resume:
{resume_text}

Job Description:
{job_description}

Rules:
- Provide clear suggestions
- Do not repeat the entire resume
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.4,
        max_tokens=600
    )

    return response.choices[0].message.content