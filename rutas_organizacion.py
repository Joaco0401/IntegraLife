"""Organizaciones del usuario y vista consolidada de tareas."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/organizaciones", tags=["Organizaciones"])


class OrganizacionDatos(BaseModel):
    nombre: str
    mi_cargo: str | None = None


def filtro_organizacion(alias: str, org: str | None, parametros: dict) -> str:
    """Construye la condicion SQL segun el filtro elegido.

    org puede ser: None/'' (todas), 'personal' (sin organizacion),
    o el id de una organizacion.
    """
    if not org or org == "todas":
        return ""
    if org == "personal":
        return f"AND {alias}.organizacion_id IS NULL"
    parametros["org"] = org
    return f"AND {alias}.organizacion_id = :org"


@router.get("")
def listar_organizaciones(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Lista las organizaciones en las que trabaja el usuario."""
    filas = db.execute(
        text("""
            SELECT o.id, o.nombre, o.mi_cargo,
                   (SELECT count(*) FROM contactos c WHERE c.organizacion_id = o.id) AS contactos
            FROM usuario_organizaciones o
            WHERE o.usuario_id = :uid
            ORDER BY o.nombre
        """),
        {"uid": uid},
    ).fetchall()
    return [
        {
            "id": str(f.id),
            "nombre": f.nombre,
            "mi_cargo": f.mi_cargo,
            "contactos": f.contactos,
        }
        for f in filas
    ]


@router.post("")
def crear_organizacion(
    datos: OrganizacionDatos,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Agrega una organizacion propia del usuario."""
    if not datos.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")
    fila = db.execute(
        text("""
            INSERT INTO usuario_organizaciones (usuario_id, nombre, mi_cargo)
            VALUES (:uid, :nombre, :cargo)
            ON CONFLICT (usuario_id, nombre) DO UPDATE SET mi_cargo = EXCLUDED.mi_cargo
            RETURNING id, nombre
        """),
        {"uid": uid, "nombre": datos.nombre.strip(), "cargo": datos.mi_cargo},
    ).fetchone()
    db.commit()
    return {"id": str(fila.id), "nombre": fila.nombre}


@router.put("/{org_id}")
def editar_organizacion(
    org_id: str,
    datos: OrganizacionDatos,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Edita el nombre o el cargo en una organizacion."""
    existe = db.execute(
        text("SELECT id FROM usuario_organizaciones WHERE id = :id AND usuario_id = :uid"),
        {"id": org_id, "uid": uid},
    ).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Organizacion no encontrada")
    db.execute(
        text("""
            UPDATE usuario_organizaciones SET nombre = :nombre, mi_cargo = :cargo
            WHERE id = :id AND usuario_id = :uid
        """),
        {"id": org_id, "uid": uid, "nombre": datos.nombre.strip(), "cargo": datos.mi_cargo},
    )
    db.commit()
    return {"mensaje": "Organizacion actualizada"}


@router.delete("/{org_id}")
def eliminar_organizacion(
    org_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina una organizacion. Los contactos quedan sin contexto, no se borran."""
    existe = db.execute(
        text("SELECT nombre FROM usuario_organizaciones WHERE id = :id AND usuario_id = :uid"),
        {"id": org_id, "uid": uid},
    ).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Organizacion no encontrada")
    db.execute(
        text("DELETE FROM usuario_organizaciones WHERE id = :id AND usuario_id = :uid"),
        {"id": org_id, "uid": uid},
    )
    db.commit()
    return {"mensaje": f"Organizacion {existe.nombre} eliminada; sus contactos quedaron sin contexto"}


@router.get("/tareas")
def tareas_consolidadas(
    org: str = "todas",
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Todas las tareas pendientes, filtradas por organizacion."""
    parametros = {"uid": uid}
    condicion = filtro_organizacion("c", org, parametros)

    filas = db.execute(
        text(f"""
            SELECT i.id AS interaccion_id, i.temas_pendientes, i.fecha,
                   c.id AS contacto_id, c.nombre AS contacto, c.cargo, c.foto_path,
                   e.nombre AS empresa, o.nombre AS organizacion
            FROM interacciones i
            JOIN contactos c ON c.id = i.contacto_id
            LEFT JOIN empresas e ON e.id = c.empresa_id
            LEFT JOIN usuario_organizaciones o ON o.id = c.organizacion_id
            WHERE i.usuario_id = :uid
              AND i.temas_pendientes IS NOT NULL
              AND jsonb_array_length(i.temas_pendientes) > 0
              {condicion}
            ORDER BY i.fecha DESC
        """),
        parametros,
    ).fetchall()

    tareas = []
    for f in filas:
        for idx, t in enumerate(f.temas_pendientes or []):
            if isinstance(t, str):
                texto_tarea, hecho = t, False
            elif isinstance(t, dict):
                texto_tarea, hecho = t.get("texto", ""), bool(t.get("hecho", False))
            else:
                continue
            if not texto_tarea:
                continue
            tareas.append({
                "interaccion_id": str(f.interaccion_id),
                "indice": idx,
                "texto": texto_tarea,
                "hecho": hecho,
                "contacto_id": str(f.contacto_id),
                "contacto": f.contacto,
                "cargo": f.cargo,
                "empresa": f.empresa,
                "organizacion": f.organizacion,
                "foto_url": f"/contactos/{f.contacto_id}/foto" if f.foto_path else None,
                "fecha": str(f.fecha),
            })

    return {
        "org": org,
        "total": len(tareas),
        "pendientes": sum(1 for t in tareas if not t["hecho"]),
        "tareas": tareas,
    }