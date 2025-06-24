from langchain_community.document_loaders import PyPDFLoader, CSVLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.faiss_manager import FAISSManager

def process_and_index_file(file_path: str, file_type: str):
    # Elegir el loader según el tipo de archivo
    if file_type == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_type == "csv":
        loader = CSVLoader(file_path)
    elif file_type in ["word", "docx"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError("Tipo de archivo no soportado")

    # Cargar documentos completos
    docs = loader.load()

    # Dividir en chunks para mejorar el análisis
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    split_docs = splitter.split_documents(docs)

    # Actualizar índice FAISS
    faiss = FAISSManager()
    faiss.create_or_update_index(split_docs)
