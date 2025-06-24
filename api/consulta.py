from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chatbot_service import get_chatbot_response

router = APIRouter()

class Consulta(BaseModel):
    question: str

@router.post("/consultar")
def hacer_consulta(consulta: Consulta):
    try:
        respuesta = get_chatbot_response(consulta.question)
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
