from database.db import SessionLocal
from database.models import Documento
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import shutil

FAISS_PATH = "backend/faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def rebuild_faiss_from_db():
    db = SessionLocal()
    documentos = db.query(Documento).all()
    db.close()

    if not documentos:
        raise ValueError("No hay documentos en la base de datos.")

    texts = [doc.contenido for doc in documentos if doc.contenido]

    # Dividir el texto
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_chunks = []
    for text in texts:
        all_chunks.extend(splitter.split_text(text))

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db_faiss = FAISS.from_texts(all_chunks, embedding=embeddings)

    # Limpiar y guardar FAISS
    if os.path.exists(FAISS_PATH):
        shutil.rmtree(FAISS_PATH)
    os.makedirs(FAISS_PATH, exist_ok=True)
    db_faiss.save_local(FAISS_PATH)

    return f"FAISS reindexado con {len(all_chunks)} fragmentos."
