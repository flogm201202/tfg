import os
import openai
from services.faiss_manager import FAISSManager
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatbot_response(query: str) -> str:
    print(f"🧠 Recibida pregunta: {query}")
    
    faiss_manager = FAISSManager()
    db = faiss_manager.load_index()

    if not db:
        print("❌ No se encontró el índice FAISS.")
        return "Todavía no hay información cargada."

    try:
        resultados = db.similarity_search(query, k=5)
        contexto = "\n".join([doc.page_content for doc in resultados])
        print(f"🔍 Fragmentos encontrados: {len(resultados)}")
        print("🧾 Contexto generado:")
        print(contexto)
    except Exception as e:
        print(f"⚠️ Error al buscar en FAISS: {e}")
        return f"Error al buscar contexto: {e}"

    prompt = f"""
Contesta la siguiente pregunta basándote solamente en la información proporcionada.
---
Información:
{contexto}
---
Pregunta: {query}
Respuesta:
""".strip()

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
        print("✅ Respuesta generada correctamente.")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error con la API de OpenAI: {e}")
        return f"Error al conectarse con OpenAI: {e}"
