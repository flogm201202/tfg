import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from services.faiss_rebuilder import rebuild_faiss_from_db
from services.document_processor import process_and_index_file
from loaders.csv_loader import load_csv
from loaders.pdf_loader import load_pdf
from loaders.word_loader import load_word
from database.db import get_db
from database.models import Documento

router = APIRouter()
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/subir")
async def subir_archivo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    tipo = ""
    contenido = ""

    if file.filename.endswith(".csv"):
        tipo = "csv"
        filas = load_csv(path)
        contenido = "\n".join(filas)

    elif file.filename.endswith(".pdf"):
        tipo = "pdf"
        contenido = load_pdf(path)

    elif file.filename.endswith(".docx"):
        tipo = "word"  
        contenido = load_word(path)

    else:
        return {"error": "Tipo de archivo no soportado"}

    # Guardar en la base de datos
    doc = Documento(
        nombre_archivo=file.filename,
        tipo=tipo,
        contenido=contenido,
        subido_por=1
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Reindexar FAISS con todo lo que hay en la base
    mensaje_reindexado = rebuild_faiss_from_db()

    # Eliminar el archivo temporal
    try:
        os.remove(path)
    except Exception as e:
        print(f"⚠️ No se pudo eliminar el archivo temporal: {e}")

    return {
        "mensaje": "Documento guardado y FAISS actualizado",
        "id": doc.id,
        "reindex": mensaje_reindexado
    }
