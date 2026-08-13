"""Endpoints de interacciones: notas de reuniones, llamadas, etc."""
import json as _json

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import SesionLocal, obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/interacciones", tags=["Interacciones"])

SQL_BUSCAR_CONTACTO = "SELECT id FROM contactos WHERE id = :id AND usuario_id = :uid"
SQL_INSERTAR = "INSERT INTO interacciones (contacto_id, tipo, contenido_raw, usuario_id) VALUES (:contacto_id, :tipo, :contenido_raw, :usuario_id) RETURNING id, fecha"
SQL_HISTORIAL = "SELECT id, tipo, fecha, contenido_raw, resumen_ia, temas_pendientes FROM interacciones WHERE contacto_id = :id AND usuario_id = :uid ORDER BY fecha DESC"
SQL_BUSCAR_INTERACCION = "SELECT i.id, i.tipo, i.contenido_raw, c.nombre FROM interacciones i JOIN contactos c ON c.id = i.contacto_id WHERE i.id = :id"
SQL_GUARDAR_RESUMEN = "UPDATE interacciones SET resumen_ia = :resumen, temas_pendientes = :temas WHERE id = :id"
SQL_LEER_TEMAS = "SELECT temas_pendientes FROM interacciones WHERE id = :id AND usuario_id = :uid"
SQL_GUARDAR_TEMAS = "UPDATE interacciones SET temas_pendientes = :temas WHERE id = :id AND usuario_id = :uid"
SQL_VERIFICAR = "SELECT id FROM interacciones WHERE id = :id AND usuario_id = :uid"


class InteraccionNueva(BaseModel):
    contacto_id: str
    tipo: str
    contenido_raw: str


class InteraccionEditar(BaseModel):
    tipo: str
    contenido_raw: str


class ToggleTema(BaseModel):
    indice: int


def normalizar_temas(temas):
    """Convierte temas al formato [{texto, hecho}], aceptando strings antiguos."""
    if not temas:
        return []
    resultado = []
    for t in temas:
        if isinstance(t, str):
            resultado.append({"texto": t, "hecho": False})
        elif isinstance(t, dict) and "texto" in t:
            resultado.append({"texto": t["texto"], "hecho": bool(t.get("hecho", False))})
    return resultado


def procesar_en_fondo(interaccion_id: str):
    """Tarea de fondo: pide el resumen a Claude y lo guarda."""
    from generador_ia import resumir_interaccion

    db = SesionLocal()
    try:
        fila = db.execute(text(SQL_BUSCAR_INTERACCION), {"id": interaccion_id}).fetchone()
        if fila is None:
            return
        resultado = resumir_interaccion(fila.nombre, fila.tipo, fila.contenido_raw)
        temas = normalizar_temas(resultado.get("temas_pendientes", []))
        db.execute(
            text(SQL_GUARDAR_RESUMEN),
            {
                "id": interaccion_id,
                "resumen": resultado.get("resumen"),
                "temas": _json.dumps(temas, ensure_ascii=False),
            },
        )
        db.commit()
        print(f"[IA] Interaccion {interaccion_id} procesada correctamente")
    except Exception as e:
        print(f"[IA] Error procesando {interaccion_id}: {e}")
    finally:
        db.close()


@router.post("")
def crear_interaccion(
    datos: InteraccionNueva,
    tareas: BackgroundTasks,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Registra una interaccion y lanza el resumen automatico con Claude."""
    existe = db.execute(
        text(SQL_BUSCAR_CONTACTO), {"id": datos.contacto_id, "uid": uid}
    ).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

    valores = datos.model_dump()
    valores["usuario_id"] = uid
    fila = db.execute(text(SQL_INSERTAR), valores).fetchone()
    db.commit()
    tareas.add_task(procesar_en_fondo, str(fila.id))
    return {
        "id": str(fila.id),
        "fecha": str(fila.fecha),
        "mensaje": "Interaccion registrada; resumen en proceso",
    }


@router.put("/{interaccion_id}")
def editar_interaccion(
    interaccion_id: str,
    datos: InteraccionEditar,
    tareas: BackgroundTasks,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Edita una anotacion y vuelve a generar su resumen y pendientes."""
    existe = db.execute(text(SQL_VERIFICAR), {"id": interaccion_id, "uid": uid}).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Interaccion no encontrada")
    if not datos.contenido_raw.strip():
        raise HTTPException(status_code=400, detail="La anotacion no puede estar vacia")

    db.execute(
        text("""
            UPDATE interacciones
            SET tipo = :tipo, contenido_raw = :contenido_raw,
                resumen_ia = NULL, temas_pendientes = '[]'::jsonb
            WHERE id = :id AND usuario_id = :uid
        """),
        {
            "id": interaccion_id,
            "uid": uid,
            "tipo": datos.tipo,
            "contenido_raw": datos.contenido_raw.strip(),
        },
    )
    db.commit()
    tareas.add_task(procesar_en_fondo, interaccion_id)
    return {"id": interaccion_id, "mensaje": "Anotacion actualizada; resumen en proceso"}


@router.delete("/{interaccion_id}")
def eliminar_interaccion(
    interaccion_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina una anotacion y sus puntos pendientes asociados."""
    existe = db.execute(text(SQL_VERIFICAR), {"id": interaccion_id, "uid": uid}).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Interaccion no encontrada")
    db.execute(
        text("DELETE FROM interacciones WHERE id = :id AND usuario_id = :uid"),
        {"id": interaccion_id, "uid": uid},
    )
    db.commit()
    return {"mensaje": "Anotacion eliminada"}


@router.get("/contacto/{contacto_id}")
def historial_contacto(
    contacto_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Historial completo de interacciones con un contacto."""
    filas = db.execute(text(SQL_HISTORIAL), {"id": contacto_id, "uid": uid}).fetchall()
    return [
        {
            "id": str(f.id),
            "tipo": f.tipo,
            "fecha": str(f.fecha),
            "contenido": f.contenido_raw,
            "resumen_ia": f.resumen_ia,
            "temas_pendientes": normalizar_temas(f.temas_pendientes),
        }
        for f in filas
    ]


@router.patch("/{interaccion_id}/tema")
def alternar_tema(
    interaccion_id: str,
    datos: ToggleTema,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Marca o desmarca un tema pendiente de una interaccion."""
    fila = db.execute(text(SQL_LEER_TEMAS), {"id": interaccion_id, "uid": uid}).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Interaccion no encontrada")

    temas = normalizar_temas(fila.temas_pendientes)
    if datos.indice < 0 or datos.indice >= len(temas):
        raise HTTPException(status_code=400, detail="Indice de tema invalido")

    temas[datos.indice]["hecho"] = not temas[datos.indice]["hecho"]
    db.execute(
        text(SQL_GUARDAR_TEMAS),
        {
            "id": interaccion_id,
            "uid": uid,
            "temas": _json.dumps(temas, ensure_ascii=False),
        },
    )
    db.commit()
    return {"temas_pendientes": temas}


@router.delete("/{interaccion_id}/tema/{indice}")
def eliminar_tema(
    interaccion_id: str,
    indice: int,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina un punto pendiente puntual, conservando la anotacion."""
    fila = db.execute(text(SQL_LEER_TEMAS), {"id": interaccion_id, "uid": uid}).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Interaccion no encontrada")

    temas = normalizar_temas(fila.temas_pendientes)
    if indice < 0 or indice >= len(temas):
        raise HTTPException(status_code=400, detail="Indice de tema invalido")

    temas.pop(indice)
    db.execute(
        text(SQL_GUARDAR_TEMAS),
        {
            "id": interaccion_id,
            "uid": uid,
            "temas": _json.dumps(temas, ensure_ascii=False),
        },
    )
    db.commit()
    return {"mensaje": "Punto eliminado", "temas_pendientes": temas}


@router.post("/{interaccion_id}/procesar")
def procesar_interaccion(
    interaccion_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Reprocesa manualmente una interaccion."""
    from generador_ia import resumir_interaccion

    existe = db.execute(text(SQL_VERIFICAR), {"id": interaccion_id, "uid": uid}).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Interaccion no encontrada")

    fila = db.execute(text(SQL_BUSCAR_INTERACCION), {"id": interaccion_id}).fetchone()
    resultado = resumir_interaccion(fila.nombre, fila.tipo, fila.contenido_raw)
    temas = normalizar_temas(resultado.get("temas_pendientes", []))
    db.execute(
        text(SQL_GUARDAR_RESUMEN),
        {
            "id": interaccion_id,
            "resumen": resultado.get("resumen"),
            "temas": _json.dumps(temas, ensure_ascii=False),
        },
    )
    db.commit()
    return {"resumen": resultado.get("resumen"), "temas_pendientes": temas}