from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chatbot_service import get_chatbot_response


router = APIRouter()

class QueryRequest(BaseModel):
    user_id: int
    role: str
    question: str

@router.post("/query")
def query_chatbot(request: QueryRequest):
    try:
        answer = get_chatbot_response(request.question)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
