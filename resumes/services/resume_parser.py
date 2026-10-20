import io

import fitz  # PyMuPDF
from docx import Document


def extract_resume_text(uploaded_file):
    """
    Read text from an uploaded resume (PDF or DOCX).
    Returns the text as a single string.
    """

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if filename.endswith(".pdf"):
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
            pages = [page.get_text() for page in pdf]
        return "\n".join(pages).strip()

    if filename.endswith(".docx"):
        document = Document(io.BytesIO(file_bytes))
        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]
        return "\n".join(paragraphs).strip()

    raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")