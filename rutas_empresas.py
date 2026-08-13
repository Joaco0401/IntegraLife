"""Endpoints de empresas."""
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/empresas", tags=["Empresas"])

CARPETA_FOTOS = Path("fotos/empresas")
CARPETA_FOTOS.mkdir(parents=True, exist_ok=True)
FORMATOS_FOTO = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_FOTO_BYTES = 5_000_000


class EmpresaDatos(BaseModel):
    nombre: str
    nicho: str | None = None
    descripcion: str | None = None
    sitio_web: str | None = None
    organizacion_id: str | None = None


def _verificar_propiedad(db: Session, empresa_id: str, uid: str):
    fila = db.execute(
        text("SELECT id, nombre, foto_path FROM empresas WHERE id = :id AND usuario_id = :uid"),
        {"id": empresa_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return fila


@router.post("")
def crear_empresa(
    datos: EmpresaDatos,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Crea una empresa nueva."""
    valores = datos.model_dump()
    valores["usuario_id"] = uid
    fila = db.execute(
        text("""
            INSERT INTO empresas (nombre, nicho, descripcion, sitio_web, organizacion_id, usuario_id)
            VALUES (:nombre, :nicho, :descripcion, :sitio_web, :organizacion_id, :usuario_id)
            RETURNING id, nombre, nicho
        """),
        valores,
    ).fetchone()
    db.commit()
    return {"id": str(fila.id), "nombre": fila.nombre, "nicho": fila.nicho}


@router.get("")
def listar_empresas(
    org: str = "todas",
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Lista las empresas del usuario, filtradas por organizacion."""
    from rutas_organizacion import filtro_organizacion

    parametros = {"uid": uid}
    condicion = filtro_organizacion("e", org, parametros)

    filas = db.execute(
        text(f"""
            SELECT e.id, e.nombre, e.nicho, e.descripcion, e.sitio_web, e.foto_path,
                   e.organizacion_id, o.nombre AS organizacion
            FROM empresas e
            LEFT JOIN usuario_organizaciones o ON o.id = e.organizacion_id
            WHERE e.usuario_id = :uid {condicion}
            ORDER BY e.nombre
        """),
        parametros,
    ).fetchall()
    return [
        {
            "id": str(f.id),
            "nombre": f.nombre,
            "nicho": f.nicho,
            "descripcion": f.descripcion,
            "sitio_web": f.sitio_web,
            "organizacion": f.organizacion,
            "organizacion_id": str(f.organizacion_id) if f.organizacion_id else None,
            "foto_url": f"/empresas/{f.id}/foto" if f.foto_path else None,
        }
        for f in filas
    ]


@router.get("/{empresa_id}")
def ver_empresa(
    empresa_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Muestra una empresa por su id."""
    fila = db.execute(
        text("""
            SELECT e.id, e.nombre, e.nicho, e.descripcion, e.sitio_web, e.foto_path,
                   e.organizacion_id, o.nombre AS organizacion
            FROM empresas e
            LEFT JOIN usuario_organizaciones o ON o.id = e.organizacion_id
            WHERE e.id = :id AND e.usuario_id = :uid
        """),
        {"id": empresa_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return {
        "id": str(fila.id),
        "nombre": fila.nombre,
        "nicho": fila.nicho,
        "descripcion": fila.descripcion,
        "sitio_web": fila.sitio_web,
        "organizacion": fila.organizacion,
        "organizacion_id": str(fila.organizacion_id) if fila.organizacion_id else None,
        "foto_url": f"/empresas/{fila.id}/foto" if fila.foto_path else None,
    }


@router.post("/{empresa_id}/foto")
async def subir_foto_empresa(
    empresa_id: str,
    foto: UploadFile = File(...),
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Sube o reemplaza la imagen de una empresa."""
    existe = _verificar_propiedad(db, empresa_id, uid)

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

    ruta = CARPETA_FOTOS / f"{empresa_id}{extension}"
    ruta.write_bytes(contenido)
    db.execute(
        text("UPDATE empresas SET foto_path = :ruta WHERE id = :id"),
        {"ruta": str(ruta), "id": empresa_id},
    )
    db.commit()
    return {"foto_url": f"/empresas/{empresa_id}/foto"}


@router.get("/{empresa_id}/foto")
def ver_foto_empresa(
    empresa_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Devuelve la imagen asociada a una empresa."""
    fila = db.execute(
        text("SELECT foto_path FROM empresas WHERE id = :id AND usuario_id = :uid"),
        {"id": empresa_id, "uid": uid},
    ).fetchone()
    if fila is None or not fila.foto_path:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    ruta = Path(fila.foto_path)
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo de foto no encontrado")
    return FileResponse(ruta)


@router.put("/{empresa_id}")
def editar_empresa(
    empresa_id: str,
    datos: EmpresaDatos,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Actualiza los datos de una empresa."""
    _verificar_propiedad(db, empresa_id, uid)

    valores = datos.model_dump()
    valores["id"] = empresa_id
    valores["uid"] = uid
    db.execute(
        text("""
            UPDATE empresas SET nombre = :nombre, nicho = :nicho,
                descripcion = :descripcion, sitio_web = :sitio_web,
                organizacion_id = :organizacion_id
            WHERE id = :id AND usuario_id = :uid
        """),
        valores,
    )
    db.commit()
    return {"id": empresa_id, "mensaje": "Empresa actualizada"}


@router.delete("/{empresa_id}")
def eliminar_empresa(
    empresa_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina una empresa. Los contactos asociados quedan sin empresa."""
    existe = _verificar_propiedad(db, empresa_id, uid)

    if existe.foto_path:
        ruta_foto = Path(existe.foto_path)
        if ruta_foto.exists():
            ruta_foto.unlink()
    db.execute(
        text("DELETE FROM empresas WHERE id = :id AND usuario_id = :uid"),
        {"id": empresa_id, "uid": uid},
    )
    db.commit()
    return {"mensaje": f"Empresa {existe.nombre} eliminada; sus contactos quedaron sin empresa"}