import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

FAISS_PATH = "backend/faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class FAISSManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    def load_index(self):
        if os.path.exists(FAISS_PATH):
            print("📦 Índice FAISS encontrado. Cargando...")
            return FAISS.load_local(FAISS_PATH, self.embeddings, allow_dangerous_deserialization=True)
        print("❌ No se encontró el índice FAISS.")
        return None

    def save_index(self, db):
        db.save_local(FAISS_PATH)
        print("💾 Índice FAISS guardado en disco.")

    def create_or_update_index(self, docs):
        db = self.load_index()
        if db:
            db.add_documents(docs)
            print(f"🟢 Se agregaron {len(docs)} documentos al índice FAISS existente.")
        else:
            db = FAISS.from_documents(docs, self.embeddings)
            print(f"🆕 Se creó un índice FAISS nuevo con {len(docs)} documentos.")
        self.save_index(db)
