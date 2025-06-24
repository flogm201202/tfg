import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

FAISS_PATH = "faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class FAISSManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    def load_index(self):
        if os.path.exists(FAISS_PATH):
            return FAISS.load_local(FAISS_PATH, self.embeddings, allow_dangerous_deserialization=True)
        else:
            return None


    def save_index(self, db):
        db.save_local(FAISS_PATH)

    def create_or_update_index(self, docs):
        db = self.load_index()
        if db:
            db.add_documents(docs)
        else:
            db = FAISS.from_documents(docs, self.embeddings)
        self.save_index(db)
