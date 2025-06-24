from sentence_transformers import SentenceTransformer
import numpy as np
from openai import OpenAI
from database.db import get_similar_chunks  # Función que implementás vos

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_chatbot_response(question, user_id, role):
    # 1. Embedding de la pregunta
    question_embedding = embedding_model.encode([question])[0]

    # 2. Buscar chunks similares
    top_chunks = get_similar_chunks(question_embedding, top_k=5)

    # 3. Armar contexto
    context = "\n".join([chunk['text'] for chunk in top_chunks])

    # 4. Armar prompt y generar respuesta
    prompt = f"""
    Contesta la siguiente pregunta de forma clara, basada solo en la información proporcionada.
    ---
    Información: 
    {context}
    ---
    Pregunta: {question}
    Respuesta:"""

    # 5. Llamada a GPT (o el modelo que uses)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = OpenAI().ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion['choices'][0]['message']['content']
