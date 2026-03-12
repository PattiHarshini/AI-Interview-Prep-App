from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question):

    prompt = f"""
Answer the following technical interview question.

Provide:

1. Clear explanation
2. Example code if applicable

Question:
{question}

Explain in a way suitable for interviews.
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.6,
        max_tokens=300
    )

    return response.choices[0].message.content