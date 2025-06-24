import fitz  # PyMuPDF

def load_pdf(path: str):
    doc = fitz.open(path)
    text = "".join(page.get_text() for page in doc)
    return text
