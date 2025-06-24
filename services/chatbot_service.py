import os
import openai
from services.faiss_manager import FAISSManager
from dotenv import load_dotenv

load_dotenv()

# Configurar la clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatbot_response(query: str) -> str:
    # Cargar índice vectorial
    faiss_manager = FAISSManager()
    db = faiss_manager.load_index()

    if not db:
        return "Todavía no hay información cargada."

    # Buscar los 5 fragmentos más relevantes
    try:
        resultados = db.similarity_search(query, k=5)
        contexto = "\n".join([doc.page_content for doc in resultados])
    except Exception as e:
        return f"Error al buscar contexto: {e}"

    # Construir el prompt con contexto
    prompt = f"""
Contesta la siguiente pregunta basándote solamente en la información proporcionada.
---
Información:
{contexto}
---
Pregunta: {query}
Respuesta:
""".strip()

    # Llamar a la API de OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos un asistente que responde solo con la información dada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al conectarse con OpenAI: {e}"
