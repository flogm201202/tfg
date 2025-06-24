from faiss_manager import FAISSManager

faiss = FAISSManager()
db = faiss.load_index()

if not db:
    print("No hay índice.")
else:
    resultados = db.similarity_search("¿Cuál es la política de licencias?", k=5)
    for r in resultados:
        print("\n", r.page_content)
