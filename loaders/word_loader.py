from docx import Document

def load_word(path: str):
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text
