"""Endpoints de contactos."""
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/contactos", tags=["Contactos"])

CARPETA_FOTOS = Path("fotos/contactos")
CARPETA_FOTOS.mkdir(parents=True, exist_ok=True)
FORMATOS_FOTO = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_FOTO_BYTES = 5_000_000


class ContactoNuevo(BaseModel):
    nombre: str
    empresa_id: str | None = None
    cargo: str | None = None
    nicho: str | None = None
    telefono: str | None = None
    linkedin_url: str | None = None
    notas_generales: str | None = None
    relacion_tipo: str | None = None
    organizacion_id: str | None = None
    emails: list[str] = []


class ContactoEditar(BaseModel):
    nombre: str
    empresa_id: str | None = None
    cargo: str | None = None
    nicho: str | None = None
    telefono: str | None = None
    linkedin_url: str | None = None
    notas_generales: str | None = None
    relacion_tipo: str | None = None
    organizacion_id: str | None = None
    emails: list[str] = []


def _verificar_propiedad(db: Session, contacto_id: str, uid: str):
    """Confirma que el contacto pertenece al usuario logueado."""
    fila = db.execute(
        text("SELECT id, foto_path, nombre FROM contactos WHERE id = :id AND usuario_id = :uid"),
        {"id": contacto_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return fila


@router.post("")
def crear_contacto(
    datos: ContactoNuevo,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Crea un contacto y registra sus emails."""
    valores = datos.model_dump(exclude={"emails"})
    valores["usuario_id"] = uid
    fila = db.execute(
        text("""
            INSERT INTO contactos
                (nombre, empresa_id, cargo, nicho, telefono,
                 linkedin_url, notas_generales, relacion_tipo, organizacion_id, usuario_id)
            VALUES
                (:nombre, :empresa_id, :cargo, :nicho, :telefono,
                 :linkedin_url, :notas_generales, :relacion_tipo, :organizacion_id, :usuario_id)
            RETURNING id, nombre
        """),
        valores,
    ).fetchone()

    for email in datos.emails:
        if email and email.strip():
            db.execute(
                text("INSERT INTO contacto_emails (contacto_id, email) VALUES (:cid, :email)"),
                {"cid": str(fila.id), "email": email.strip().lower()},
            )

    db.commit()
    return {"id": str(fila.id), "nombre": fila.nombre, "emails": datos.emails}


@router.get("")
def listar_contactos(
    org: str = "todas",
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Lista los contactos con sus pendientes abiertos y ultimo contacto."""
    from rutas_organizacion import filtro_organizacion

    parametros = {"uid": uid}
    condicion = filtro_organizacion("c", org, parametros)

    filas = db.execute(
        text(f"""
            SELECT c.id, c.nombre, c.cargo, c.relacion_tipo, c.relacion_estado,
                   c.foto_path, c.empresa_id, c.organizacion_id,
                   e.nombre AS empresa, o.nombre AS organizacion,
                   (SELECT max(i.fecha) FROM interacciones i
                     WHERE i.contacto_id = c.id) AS ultimo_contacto,
                   COALESCE((
                     SELECT count(*) FROM interacciones i,
                            jsonb_array_elements(i.temas_pendientes) t
                     WHERE i.contacto_id = c.id
                       AND i.temas_pendientes IS NOT NULL
                       AND COALESCE((t->>'hecho')::boolean, false) = false
                   ), 0) AS pendientes
            FROM contactos c
            LEFT JOIN empresas e ON e.id = c.empresa_id
            LEFT JOIN usuario_organizaciones o ON o.id = c.organizacion_id
            WHERE c.usuario_id = :uid {condicion}
            ORDER BY c.nombre
        """),
        parametros,
    ).fetchall()
    return [
        {
            "id": str(f.id),
            "nombre": f.nombre,
            "cargo": f.cargo,
            "empresa": f.empresa,
            "empresa_id": str(f.empresa_id) if f.empresa_id else None,
            "organizacion": f.organizacion,
            "organizacion_id": str(f.organizacion_id) if f.organizacion_id else None,
            "relacion_tipo": f.relacion_tipo,
            "relacion_estado": f.relacion_estado,
            "foto_url": f"/contactos/{f.id}/foto" if f.foto_path else None,
            "pendientes": f.pendientes,
            "ultimo_contacto": str(f.ultimo_contacto) if f.ultimo_contacto else None,
        }
        for f in filas
    ]


@router.get("/{contacto_id}")
def ver_contacto(
    contacto_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Ficha completa de un contacto del usuario logueado."""
    fila = db.execute(
        text("""
            SELECT c.id, c.nombre, c.cargo, c.nicho, c.telefono, c.linkedin_url,
                   c.notas_generales, c.relacion_tipo, c.relacion_estado, c.foto_path,
                   c.empresa_id, c.organizacion_id,
                   e.nombre AS empresa, o.nombre AS organizacion
            FROM contactos c
            LEFT JOIN empresas e ON e.id = c.empresa_id
            LEFT JOIN usuario_organizaciones o ON o.id = c.organizacion_id
            WHERE c.id = :id AND c.usuario_id = :uid
        """),
        {"id": contacto_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

    emails = db.execute(
        text("SELECT email FROM contacto_emails WHERE contacto_id = :id"),
        {"id": contacto_id},
    ).fetchall()

    interacciones = db.execute(
        text("""
            SELECT tipo, fecha, resumen_ia, contenido_raw
            FROM interacciones
            WHERE contacto_id = :id
            ORDER BY fecha DESC
            LIMIT 5
        """),
        {"id": contacto_id},
    ).fetchall()

    return {
        "id": str(fila.id),
        "nombre": fila.nombre,
        "cargo": fila.cargo,
        "empresa": fila.empresa,
        "empresa_id": str(fila.empresa_id) if fila.empresa_id else None,
        "organizacion": fila.organizacion,
        "organizacion_id": str(fila.organizacion_id) if fila.organizacion_id else None,
        "nicho": fila.nicho,
        "telefono": fila.telefono,
        "linkedin_url": fila.linkedin_url,
        "notas_generales": fila.notas_generales,
        "relacion_tipo": fila.relacion_tipo,
        "relacion_estado": fila.relacion_estado,
        "foto_url": f"/contactos/{fila.id}/foto" if fila.foto_path else None,
        "emails": [e.email for e in emails],
        "ultimas_interacciones": [
            {
                "tipo": i.tipo,
                "fecha": str(i.fecha),
                "resumen": i.resumen_ia or i.contenido_raw[:200],
            }
            for i in interacciones
        ],
    }


@router.post("/{contacto_id}/foto")
async def subir_foto_contacto(
    contacto_id: str,
    foto: UploadFile = File(...),
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Sube o reemplaza la foto de perfil de un contacto."""
    existe = _verificar_propiedad(db, contacto_id, uid)

    tipo = (foto.content_type or "").lower()
    extension = FORMATOS_FOTO.get(tipo)
    if extension is None:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa JPG, PNG o WEBP")

    contenido = await foto.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="La imagen esta vacia")
    if len(contenido) > MAX_FOTO_BYTES:
        raise HTTPException(status_code=400, detail="La imagen supera el maximo de 5 MB")

    if existe.foto_path:
        anterior = Path(existe.foto_path)
        if anterior.exists():
            anterior.unlink()

    ruta = CARPETA_FOTOS / f"{contacto_id}{extension}"
    ruta.write_bytes(contenido)
    db.execute(
        text("UPDATE contactos SET foto_path = :ruta WHERE id = :id"),
        {"ruta": str(ruta), "id": contacto_id},
    )
    db.commit()
    return {"foto_url": f"/contactos/{contacto_id}/foto"}


@router.get("/{contacto_id}/foto")
def ver_foto_contacto(
    contacto_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Devuelve la foto de perfil de un contacto."""
    fila = db.execute(
        text("SELECT foto_path FROM contactos WHERE id = :id AND usuario_id = :uid"),
        {"id": contacto_id, "uid": uid},
    ).fetchone()
    if fila is None or not fila.foto_path:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    ruta = Path(fila.foto_path)
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo de foto no encontrado")
    return FileResponse(ruta)


@router.put("/{contacto_id}")
def editar_contacto(
    contacto_id: str,
    datos: ContactoEditar,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Actualiza los datos de un contacto y reemplaza sus emails."""
    _verificar_propiedad(db, contacto_id, uid)

    valores = datos.model_dump(exclude={"emails"})
    valores["id"] = contacto_id
    valores["uid"] = uid
    db.execute(
        text("""
            UPDATE contactos SET nombre = :nombre, empresa_id = :empresa_id,
                cargo = :cargo, nicho = :nicho, telefono = :telefono,
                linkedin_url = :linkedin_url, notas_generales = :notas_generales,
                relacion_tipo = :relacion_tipo, organizacion_id = :organizacion_id
            WHERE id = :id AND usuario_id = :uid
        """),
        valores,
    )

    db.execute(
        text("DELETE FROM contacto_emails WHERE contacto_id = :id"), {"id": contacto_id}
    )
    for email in datos.emails:
        if email and email.strip():
            db.execute(
                text("INSERT INTO contacto_emails (contacto_id, email) VALUES (:cid, :email)"),
                {"cid": contacto_id, "email": email.strip().lower()},
            )

    db.commit()
    return {"id": contacto_id, "mensaje": "Contacto actualizado"}


@router.delete("/{contacto_id}")
def eliminar_contacto(
    contacto_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina un contacto y toda su informacion asociada."""
    existe = _verificar_propiedad(db, contacto_id, uid)

    if existe.foto_path:
        ruta_foto = Path(existe.foto_path)
        if ruta_foto.exists():
            ruta_foto.unlink()
    db.execute(
        text("DELETE FROM contactos WHERE id = :id AND usuario_id = :uid"),
        {"id": contacto_id, "uid": uid},
    )
    db.commit()
    return {"mensaje": f"Contacto {existe.nombre} eliminado con toda su informacion"}