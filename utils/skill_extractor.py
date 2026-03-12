import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(resume_text, job_description):

    text = resume_text + " " + job_description

    doc = nlp(text)

    skills = set()

    for token in doc:

        # Capture nouns and proper nouns (often technologies)
        if token.pos_ in ["PROPN", "NOUN"]:

            word = token.text.lower()

            if len(word) > 2:
                skills.add(word)

    return list(skills)