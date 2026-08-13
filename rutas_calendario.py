"""Endpoints de calendario: sincronizar, consultar agenda y eventos locales."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/calendario", tags=["Calendario"])

SQL_UPSERT_EVENTO = """
INSERT INTO eventos (gcal_event_id, titulo, descripcion, ubicacion, inicio, fin, link_reunion, usuario_id)
VALUES (:gcal_event_id, :titulo, :descripcion, :ubicacion, :inicio, :fin, :link_reunion, :usuario_id)
ON CONFLICT (gcal_event_id, usuario_id) DO UPDATE SET
  titulo = EXCLUDED.titulo, descripcion = EXCLUDED.descripcion,
  ubicacion = EXCLUDED.ubicacion, inicio = EXCLUDED.inicio,
  fin = EXCLUDED.fin, link_reunion = EXCLUDED.link_reunion,
  sincronizado_en = now()
RETURNING id
"""
SQL_UPSERT_ASISTENTE = """
INSERT INTO evento_asistentes (evento_id, email, nombre, contacto_id)
VALUES (:evento_id, :email, :nombre,
        (SELECT ce.contacto_id FROM contacto_emails ce
         JOIN contactos c ON c.id = ce.contacto_id
         WHERE lower(ce.email) = lower(:email) AND c.usuario_id = :usuario_id
         LIMIT 1))
ON CONFLICT (evento_id, email) DO UPDATE SET
  nombre = EXCLUDED.nombre,
  contacto_id = EXCLUDED.contacto_id
"""
SQL_OCULTOS = "SELECT gcal_event_id FROM eventos_ocultos WHERE usuario_id = :uid"
SQL_AGENDA = """
SELECT e.id, e.titulo, e.descripcion, e.ubicacion, e.inicio, e.fin, e.link_reunion,
       e.gcal_event_id, e.organizacion_id, o.nombre AS organizacion,
       COALESCE(json_agg(json_build_object(
           'email', a.email, 'nombre', COALESCE(c.nombre, a.nombre),
           'contacto_id', a.contacto_id
       )) FILTER (WHERE a.id IS NOT NULL), '[]') AS asistentes
FROM eventos e
LEFT JOIN evento_asistentes a ON a.evento_id = e.id
LEFT JOIN contactos c ON c.id = a.contacto_id
LEFT JOIN usuario_organizaciones o ON o.id = e.organizacion_id
WHERE e.usuario_id = :uid
  AND e.inicio >= CURRENT_DATE
  AND e.inicio < CURRENT_DATE + (:dias || ' days')::interval
  {condicion}
GROUP BY e.id, o.nombre
ORDER BY e.inicio
"""
SQL_EVENTOS_CONTACTO = """
SELECT e.id, e.titulo, e.ubicacion, e.inicio, e.fin, e.link_reunion
FROM eventos e
JOIN evento_asistentes a ON a.evento_id = e.id
WHERE a.contacto_id = :contacto_id AND e.usuario_id = :uid
ORDER BY e.inicio DESC
LIMIT 20
"""


class EventoLocal(BaseModel):
    titulo: str
    fecha: str
    hora: str | None = None
    contacto_id: str | None = None
    descripcion: str | None = None
    organizacion_id: str | None = None


class EventoEditar(BaseModel):
    titulo: str
    fecha: str
    hora: str | None = None
    descripcion: str | None = None
    ubicacion: str | None = None
    organizacion_id: str | None = None


def sincronizar_para_usuario(db: Session, uid: str, dias: int = 7) -> int:
    """Sincroniza Google Calendar respetando los eventos ocultados."""
    from calendario_google import traer_eventos

    ocultos = {
        f.gcal_event_id
        for f in db.execute(text(SQL_OCULTOS), {"uid": uid}).fetchall()
    }

    eventos = traer_eventos(dias=dias)
    guardados = 0
    for ev in eventos:
        if ev["gcal_event_id"] in ocultos:
            continue
        fila = db.execute(text(SQL_UPSERT_EVENTO), {
            "gcal_event_id": ev["gcal_event_id"],
            "titulo": ev["titulo"],
            "descripcion": ev["descripcion"],
            "ubicacion": ev["ubicacion"],
            "inicio": ev["inicio"],
            "fin": ev["fin"],
            "link_reunion": ev["link_reunion"],
            "usuario_id": uid,
        }).fetchone()
        for a in ev["asistentes"]:
            if a.get("email"):
                db.execute(text(SQL_UPSERT_ASISTENTE), {
                    "evento_id": str(fila.id),
                    "email": a["email"],
                    "nombre": a.get("nombre"),
                    "usuario_id": uid,
                })
        guardados += 1
    db.commit()
    return guardados


@router.post("/sincronizar")
def sincronizar(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Trae los eventos de Google Calendar para el usuario actual."""
    guardados = sincronizar_para_usuario(db, uid)
    return {"mensaje": f"{guardados} eventos sincronizados"}


@router.post("/evento")
def crear_evento_local(
    datos: EventoLocal,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Crea un evento local propio del usuario."""
    hora = datos.hora or "09:00"
    inicio = f"{datos.fecha} {hora}:00"

    fila = db.execute(text(SQL_UPSERT_EVENTO), {
        "gcal_event_id": "local-" + str(uuid.uuid4()),
        "titulo": datos.titulo,
        "descripcion": datos.descripcion,
        "ubicacion": None,
        "inicio": inicio,
        "fin": None,
        "link_reunion": None,
        "usuario_id": uid,
    }).fetchone()

    if datos.organizacion_id:
        db.execute(
            text("UPDATE eventos SET organizacion_id = :org WHERE id = :id"),
            {"org": datos.organizacion_id, "id": str(fila.id)},
        )

    if datos.contacto_id:
        contacto = db.execute(
            text("SELECT nombre FROM contactos WHERE id = :id AND usuario_id = :uid"),
            {"id": datos.contacto_id, "uid": uid},
        ).fetchone()
        if contacto is None:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        db.execute(
            text("""
                INSERT INTO evento_asistentes (evento_id, email, nombre, contacto_id)
                VALUES (:evento_id, NULL, :nombre, :contacto_id)
            """),
            {
                "evento_id": str(fila.id),
                "nombre": contacto.nombre,
                "contacto_id": datos.contacto_id,
            },
        )

    db.commit()
    return {"id": str(fila.id), "mensaje": "Evento creado en la agenda"}


@router.get("/agenda")
def agenda(
    dias: int = 1,
    org: str = "todas",
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Agenda de los proximos N dias, filtrada por organizacion."""
    parametros = {"dias": dias, "uid": uid}
    condicion = ""
    if org == "personal":
        condicion = ("AND e.organizacion_id IS NULL AND NOT EXISTS "
                     "(SELECT 1 FROM evento_asistentes ea JOIN contactos ct ON ct.id = ea.contacto_id "
                     "WHERE ea.evento_id = e.id AND ct.organizacion_id IS NOT NULL)")
    elif org and org != "todas":
        parametros["org"] = org
        condicion = ("AND (e.organizacion_id = :org OR EXISTS "
                     "(SELECT 1 FROM evento_asistentes ea JOIN contactos ct ON ct.id = ea.contacto_id "
                     "WHERE ea.evento_id = e.id AND ct.organizacion_id = :org))")

    filas = db.execute(text(SQL_AGENDA.format(condicion=condicion)), parametros).fetchall()
    return [
        {
            "id": str(f.id),
            "titulo": f.titulo,
            "descripcion": f.descripcion,
            "ubicacion": f.ubicacion,
            "inicio": str(f.inicio),
            "fin": str(f.fin) if f.fin else None,
            "link_reunion": f.link_reunion,
            "organizacion": f.organizacion,
            "organizacion_id": str(f.organizacion_id) if f.organizacion_id else None,
            "es_google": not str(f.gcal_event_id).startswith("local-"),
            "asistentes": f.asistentes,
        }
        for f in filas
    ]


@router.put("/evento/{evento_id}")
def editar_evento(
    evento_id: str,
    datos: EventoEditar,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Edita un evento. En los de Google, los cambios se pierden al sincronizar."""
    fila = db.execute(
        text("SELECT gcal_event_id FROM eventos WHERE id = :id AND usuario_id = :uid"),
        {"id": evento_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    hora = datos.hora or "09:00"
    db.execute(
        text("""
            UPDATE eventos SET titulo = :titulo, inicio = :inicio,
                descripcion = :descripcion, ubicacion = :ubicacion,
                organizacion_id = :organizacion_id
            WHERE id = :id AND usuario_id = :uid
        """),
        {
            "id": evento_id,
            "uid": uid,
            "titulo": datos.titulo,
            "inicio": f"{datos.fecha} {hora}:00",
            "descripcion": datos.descripcion,
            "ubicacion": datos.ubicacion,
            "organizacion_id": datos.organizacion_id,
        },
    )
    db.commit()
    es_google = not str(fila.gcal_event_id).startswith("local-")
    return {
        "mensaje": "Evento actualizado",
        "advertencia": ("Este evento viene de Google Calendar: los cambios se perderan "
                        "en la proxima sincronizacion." if es_google else None),
    }


@router.delete("/evento/{evento_id}")
def eliminar_evento(
    evento_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina un evento. Si viene de Google, queda registrado como oculto
    para que no reaparezca en las proximas sincronizaciones."""
    fila = db.execute(
        text("SELECT titulo, gcal_event_id FROM eventos WHERE id = :id AND usuario_id = :uid"),
        {"id": evento_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    es_google = not str(fila.gcal_event_id).startswith("local-")
    if es_google:
        db.execute(
            text("""
                INSERT INTO eventos_ocultos (usuario_id, gcal_event_id, titulo)
                VALUES (:uid, :gid, :titulo)
                ON CONFLICT (usuario_id, gcal_event_id) DO NOTHING
            """),
            {"uid": uid, "gid": fila.gcal_event_id, "titulo": fila.titulo},
        )

    db.execute(
        text("DELETE FROM eventos WHERE id = :id AND usuario_id = :uid"),
        {"id": evento_id, "uid": uid},
    )
    db.commit()
    return {
        "mensaje": f"Evento {fila.titulo} eliminado",
        "oculto_permanente": es_google,
    }


@router.get("/ocultos")
def listar_ocultos(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Eventos de Google que fueron eliminados y no vuelven a importarse."""
    filas = db.execute(
        text("""
            SELECT id, gcal_event_id, titulo, ocultado_en
            FROM eventos_ocultos WHERE usuario_id = :uid
            ORDER BY ocultado_en DESC
        """),
        {"uid": uid},
    ).fetchall()
    return [
        {
            "id": str(f.id),
            "gcal_event_id": f.gcal_event_id,
            "titulo": f.titulo,
            "ocultado_en": str(f.ocultado_en),
        }
        for f in filas
    ]


@router.delete("/ocultos/{oculto_id}")
def restaurar_oculto(
    oculto_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Quita un evento de la lista de ocultos: volvera en la proxima sincronizacion."""
    fila = db.execute(
        text("SELECT titulo FROM eventos_ocultos WHERE id = :id AND usuario_id = :uid"),
        {"id": oculto_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.execute(
        text("DELETE FROM eventos_ocultos WHERE id = :id AND usuario_id = :uid"),
        {"id": oculto_id, "uid": uid},
    )
    db.commit()
    return {"mensaje": f"{fila.titulo} volvera a aparecer en la proxima sincronizacion"}


@router.get("/contacto/{contacto_id}")
def eventos_de_contacto(
    contacto_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Reuniones vinculadas a un contacto del usuario actual."""
    filas = db.execute(
        text(SQL_EVENTOS_CONTACTO), {"contacto_id": contacto_id, "uid": uid}
    ).fetchall()
    return [
        {
            "id": str(f.id),
            "titulo": f.titulo,
            "ubicacion": f.ubicacion,
            "inicio": str(f.inicio),
            "fin": str(f.fin) if f.fin else None,
            "link_reunion": f.link_reunion,
        }
        for f in filas
    ]