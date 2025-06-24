from fastapi import APIRouter

router = APIRouter()

@router.get("/consultar")
def consultar():
    return {"msg": "consultas disponibles para empleados"}
