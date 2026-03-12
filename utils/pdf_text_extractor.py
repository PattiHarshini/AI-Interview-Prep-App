# utils/pdf_text_extractor.py

import PyPDF2

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file (Streamlit UploadedFile object).
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""