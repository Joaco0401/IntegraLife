"""Panorama del dia: agenda, pendientes y relaciones que necesitan atencion."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/hoy", tags=["Hoy"])


@router.get("")
def panorama_hoy(
    org: str = "todas",
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Todo lo que el usuario necesita saber al empezar el dia."""
    parametros = {"uid": uid}

    cond_ev = ""
    cond_c = ""
    if org == "personal":
        cond_ev = ("AND e.organizacion_id IS NULL AND NOT EXISTS "
                   "(SELECT 1 FROM evento_asistentes ea JOIN contactos ct ON ct.id = ea.contacto_id "
                   "WHERE ea.evento_id = e.id AND ct.organizacion_id IS NOT NULL)")
        cond_c = "AND c.organizacion_id IS NULL"
    elif org and org != "todas":
        parametros["org"] = org
        cond_ev = ("AND (e.organizacion_id = :org OR EXISTS "
                   "(SELECT 1 FROM evento_asistentes ea JOIN contactos ct ON ct.id = ea.contacto_id "
                   "WHERE ea.evento_id = e.id AND ct.organizacion_id = :org))")
        cond_c = "AND c.organizacion_id = :org"

    eventos = db.execute(
        text(f"""
            SELECT e.id, e.titulo, e.inicio, e.ubicacion, e.descripcion,
                   COALESCE(json_agg(json_build_object(
                       'nombre', COALESCE(c.nombre, a.nombre),
                       'contacto_id', a.contacto_id
                   )) FILTER (WHERE a.id IS NOT NULL), '[]') AS asistentes
            FROM eventos e
            LEFT JOIN evento_asistentes a ON a.evento_id = e.id
            LEFT JOIN contactos c ON c.id = a.contacto_id
            WHERE e.usuario_id = :uid
              AND e.inicio >= CURRENT_DATE
              AND e.inicio < CURRENT_DATE + interval '2 days'
              {cond_ev}
            GROUP BY e.id
            ORDER BY e.inicio
        """),
        parametros,
    ).fetchall()

    filas_pend = db.execute(
        text(f"""
            SELECT i.id AS interaccion_id, i.fecha, i.temas_pendientes,
                   c.id AS contacto_id, c.nombre AS contacto, c.foto_path,
                   emp.nombre AS empresa
            FROM interacciones i
            JOIN contactos c ON c.id = i.contacto_id
            LEFT JOIN empresas emp ON emp.id = c.empresa_id
            WHERE i.usuario_id = :uid
              AND i.temas_pendientes IS NOT NULL
              AND jsonb_array_length(i.temas_pendientes) > 0
              {cond_c}
            ORDER BY i.fecha DESC
            LIMIT 60
        """),
        parametros,
    ).fetchall()

    pendientes = []
    for f in filas_pend:
        for idx, t in enumerate(f.temas_pendientes or []):
            if isinstance(t, str):
                texto_tarea, hecho = t, False
            elif isinstance(t, dict):
                texto_tarea, hecho = t.get("texto", ""), bool(t.get("hecho", False))
            else:
                continue
            if not texto_tarea or hecho:
                continue
            pendientes.append({
                "interaccion_id": str(f.interaccion_id),
                "indice": idx,
                "texto": texto_tarea,
                "contacto_id": str(f.contacto_id),
                "contacto": f.contacto,
                "empresa": f.empresa,
                "foto_url": f"/contactos/{f.contacto_id}/foto" if f.foto_path else None,
                "fecha": str(f.fecha),
            })

    sin_contacto = db.execute(
        text(f"""
            SELECT c.id, c.nombre, c.cargo, c.foto_path, emp.nombre AS empresa,
                   (SELECT max(i.fecha) FROM interacciones i WHERE i.contacto_id = c.id) AS ultimo
            FROM contactos c
            LEFT JOIN empresas emp ON emp.id = c.empresa_id
            WHERE c.usuario_id = :uid {cond_c}
            ORDER BY ultimo NULLS FIRST
            LIMIT 6
        """),
        parametros,
    ).fetchall()

    resumen = db.execute(
        text(f"""
            SELECT
              (SELECT count(*) FROM eventos e WHERE e.usuario_id = :uid
                 AND e.inicio >= CURRENT_DATE AND e.inicio < CURRENT_DATE + interval '1 day') AS eventos_hoy,
              (SELECT count(*) FROM contactos c WHERE c.usuario_id = :uid {cond_c}) AS total_contactos
        """),
        parametros,
    ).fetchone()

    return {
        "eventos": [
            {
                "id": str(e.id),
                "titulo": e.titulo,
                "inicio": str(e.inicio),
                "ubicacion": e.ubicacion,
                "descripcion": e.descripcion,
                "asistentes": e.asistentes,
            }
            for e in eventos
        ],
        "pendientes": pendientes[:25],
        "total_pendientes": len(pendientes),
        "sin_contacto_reciente": [
            {
                "id": str(s.id),
                "nombre": s.nombre,
                "cargo": s.cargo,
                "empresa": s.empresa,
                "foto_url": f"/contactos/{s.id}/foto" if s.foto_path else None,
                "ultimo": str(s.ultimo) if s.ultimo else None,
            }
            for s in sin_contacto
        ],
        "eventos_hoy": resumen.eventos_hoy,
        "total_contactos": resumen.total_contactos,
    }