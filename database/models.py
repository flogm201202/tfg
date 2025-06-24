from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime
from .db import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    nombre_archivo = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # csv, pdf, docx
    contenido = Column(Text, nullable=False)  # cada fila del CSV
    fecha_subida = Column(DateTime, default=datetime.utcnow)
    subido_por = Column(Integer)  # si tenés auth, podés usar ForeignKey
