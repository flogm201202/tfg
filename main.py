from fastapi import FastAPI
from api import admin, empleado, consulta
import nltk
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

app = FastAPI()

app.include_router(admin.router, prefix="/admin")
app.include_router(empleado.router, prefix="/empleado")
app.include_router(consulta.router, prefix="/admin")     # /admin/consultar
app.include_router(consulta.router, prefix="/empleado")   # /empleado/consultar

@app.get("/")
def root():
    return {"msg": "Backend funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
