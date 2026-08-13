"""Perfil del usuario logueado."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/perfil", tags=["Perfil"])


class PerfilDatos(BaseModel):
    nombre_visible: str | None = None
    email: str | None = None
    telefono: str | None = None


@router.get("")
def ver_perfil(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Datos del usuario logueado y sus estadisticas."""
    fila = db.execute(
        text("""
            SELECT username, nombre_visible, email, telefono, creado_en
            FROM usuarios WHERE id = :uid
        """),
        {"uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    stats = db.execute(
        text("""
            SELECT
              (SELECT count(*) FROM contactos WHERE usuario_id = :uid) AS contactos,
              (SELECT count(*) FROM empresas WHERE usuario_id = :uid) AS empresas,
              (SELECT count(*) FROM interacciones WHERE usuario_id = :uid) AS anotaciones,
              (SELECT count(*) FROM usuario_organizaciones WHERE usuario_id = :uid) AS organizaciones
        """),
        {"uid": uid},
    ).fetchone()

    return {
        "username": fila.username,
        "nombre_visible": fila.nombre_visible,
        "email": fila.email,
        "telefono": fila.telefono,
        "creado_en": str(fila.creado_en),
        "estadisticas": {
            "contactos": stats.contactos,
            "empresas": stats.empresas,
            "anotaciones": stats.anotaciones,
            "organizaciones": stats.organizaciones,
        },
    }


@router.put("")
def editar_perfil(
    datos: PerfilDatos,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Actualiza los datos personales del usuario."""
    db.execute(
        text("""
            UPDATE usuarios SET nombre_visible = :nombre, email = :email, telefono = :telefono
            WHERE id = :uid
        """),
        {
            "uid": uid,
            "nombre": datos.nombre_visible,
            "email": datos.email,
            "telefono": datos.telefono,
        },
    )
    db.commit()
    return {"mensaje": "Perfil actualizado"}