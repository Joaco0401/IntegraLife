"""Conexión a PostgreSQL para Proyecto Papa."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SesionLocal = sessionmaker(bind=engine, autoflush=False)


def obtener_sesion():
    """Entrega una sesión de base de datos y la cierra al terminar."""
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()