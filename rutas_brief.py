"""Brief matutino: resumen ejecutivo del dia generado por Claude."""
import json as _json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import SesionLocal, obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/brief", tags=["Brief"])

DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def recopilar_contexto(db: Session, uid: str) -> dict:
    """Junta la agenda del dia, el contexto de los asistentes y los pendientes."""
    usuario = db.execute(
        text("SELECT username, nombre_visible FROM usuarios WHERE id = :uid"),
        {"uid": uid},
    ).fetchone()
    nombre = (usuario.nombre_visible or usuario.username) if usuario else "usuario"

    orgs = [
        f.nombre
        for f in db.execute(
            text("SELECT nombre FROM usuario_organizaciones WHERE usuario_id = :uid"),
            {"uid": uid},
        ).fetchall()
    ]

    filas_ev = db.execute(
        text("""
            SELECT e.id, e.titulo, e.inicio, e.ubicacion,
                   COALESCE(json_agg(json_build_object(
                       'nombre', COALESCE(c.nombre, a.nombre),
                       'contacto_id', a.contacto_id
                   )) FILTER (WHERE a.id IS NOT NULL), '[]') AS asistentes
            FROM eventos e
            LEFT JOIN evento_asistentes a ON a.evento_id = e.id
            LEFT JOIN contactos c ON c.id = a.contacto_id
            WHERE e.usuario_id = :uid
              AND e.inicio >= CURRENT_DATE
              AND e.inicio < CURRENT_DATE + interval '1 day'
            GROUP BY e.id
            ORDER BY e.inicio
        """),
        {"uid": uid},
    ).fetchall()

    eventos = []
    for f in filas_ev:
        nombres = [a["nombre"] for a in (f.asistentes or []) if a.get("nombre")]
        ids = [a["contacto_id"] for a in (f.asistentes or []) if a.get("contacto_id")]
        contexto = ""
        if ids:
            resumenes = db.execute(
                text("""
                    SELECT c.nombre, i.resumen_ia
                    FROM interacciones i
                    JOIN contactos c ON c.id = i.contacto_id
                    WHERE i.contacto_id = ANY(:ids) AND i.resumen_ia IS NOT NULL
                    ORDER BY i.fecha DESC
                    LIMIT 4
                """),
                {"ids": ids},
            ).fetchall()
            contexto = " | ".join(f"{r.nombre}: {r.resumen_ia}" for r in resumenes)
        hora = f.inicio.strftime("%H:%M")
        if hora == "00:00":
            hora = "todo el dia"
        eventos.append({
            "hora": hora,
            "titulo": f.titulo,
            "ubicacion": f.ubicacion,
            "asistentes": nombres,
            "contexto": contexto[:600],
        })

    filas_p = db.execute(
        text("""
            SELECT i.temas_pendientes, i.fecha, c.nombre AS contacto,
                   emp.nombre AS empresa
            FROM interacciones i
            JOIN contactos c ON c.id = i.contacto_id
            LEFT JOIN empresas emp ON emp.id = c.empresa_id
            WHERE i.usuario_id = :uid
              AND i.temas_pendientes IS NOT NULL
              AND jsonb_array_length(i.temas_pendientes) > 0
            ORDER BY i.fecha DESC
            LIMIT 40
        """),
        {"uid": uid},
    ).fetchall()

    pendientes = []
    ahora = datetime.now()
    for f in filas_p:
        try:
            dias = (ahora - f.fecha.replace(tzinfo=None)).days
        except Exception:
            dias = 0
        for t in f.temas_pendientes or []:
            texto_t = t if isinstance(t, str) else (t.get("texto") if isinstance(t, dict) else "")
            hecho = isinstance(t, dict) and t.get("hecho")
            if texto_t and not hecho:
                pendientes.append({
                    "texto": texto_t,
                    "contacto": f.contacto,
                    "empresa": f.empresa,
                    "dias": dias,
                })

    hoy = datetime.now()
    fecha_texto = f"{DIAS[hoy.weekday()]} {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"

    return {
        "nombre": nombre,
        "fecha_texto": fecha_texto,
        "eventos": eventos,
        "pendientes": pendientes,
        "organizaciones": orgs,
    }


def generar_para_usuario(db: Session, uid: str) -> dict:
    """Genera y guarda el brief del dia para un usuario."""
    from generador_ia import generar_brief_diario

    ctx = recopilar_contexto(db, uid)
    brief = generar_brief_diario(
        ctx["nombre"], ctx["fecha_texto"], ctx["eventos"],
        ctx["pendientes"], ctx["organizaciones"],
    )
    brief["fecha_texto"] = ctx["fecha_texto"]
    brief["total_eventos"] = len(ctx["eventos"])
    brief["total_pendientes"] = len(ctx["pendientes"])

    db.execute(
        text("""
            INSERT INTO briefs_generados (tipo, fecha, evento_id, contenido, modelo_usado)
            VALUES ('brief_diario', CURRENT_DATE, NULL, :cont, 'claude-sonnet-4-6')
            ON CONFLICT (tipo, fecha, evento_id) DO UPDATE
              SET contenido = EXCLUDED.contenido, generado_en = now()
        """),
        {"cont": _json.dumps(brief, ensure_ascii=False)},
    )
    db.commit()
    return brief


@router.get("")
def ver_brief(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Devuelve el brief de hoy si ya existe."""
    fila = db.execute(
        text("""
            SELECT contenido, generado_en FROM briefs_generados
            WHERE tipo = 'brief_diario' AND fecha = CURRENT_DATE AND evento_id IS NULL
        """)
    ).fetchone()
    if fila is None:
        return {"existe": False}
    contenido = fila.contenido
    if isinstance(contenido, str):
        contenido = _json.loads(contenido)
    contenido["existe"] = True
    contenido["generado_en"] = str(fila.generado_en)
    return contenido


@router.post("/generar")
def generar_brief(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Genera el brief del dia bajo demanda."""
    try:
        return generar_para_usuario(db, uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el brief: {e}")


def generar_brief_automatico():
    """Job de las 6 AM: genera el brief del usuario principal."""
    db = SesionLocal()
    try:
        usuario = db.execute(
            text("SELECT id FROM usuarios WHERE username = 'rodrigo'")
        ).fetchone()
        if usuario is None:
            return
        generar_para_usuario(db, str(usuario.id))
        print("[BRIEF] Brief matutino generado")
    except Exception as e:
        print(f"[BRIEF] Error generando el brief: {e}")
    finally:
        db.close()