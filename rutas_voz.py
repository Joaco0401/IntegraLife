"""Notas de voz: subir audio, transcribir y distribuir la informacion."""
import json as _json
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import obtener_sesion
from autenticacion import usuario_actual

router = APIRouter(prefix="/voz", tags=["Notas de voz"])

CARPETA_AUDIO = Path("audios")
CARPETA_AUDIO.mkdir(parents=True, exist_ok=True)
FORMATOS_AUDIO = {
    "audio/webm": ".webm", "audio/ogg": ".ogg", "audio/mpeg": ".mp3",
    "audio/mp4": ".m4a", "audio/x-m4a": ".m4a", "audio/wav": ".wav",
    "audio/x-wav": ".wav", "video/webm": ".webm",
}
MAX_AUDIO_BYTES = 25_000_000


class Transcripcion(BaseModel):
    transcripcion: str


@router.post("/subir")
async def subir_audio(
    audio: UploadFile = File(...),
    duracion: int = Form(0),
    org: str = Form(""),
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Guarda el audio y lo transcribe automaticamente con Whisper."""
    from transcriptor import transcribir, hay_transcriptor

    tipo = (audio.content_type or "").lower().split(";")[0]
    extension = FORMATOS_AUDIO.get(tipo)
    if extension is None:
        nombre = (audio.filename or "").lower()
        for ext in (".webm", ".ogg", ".mp3", ".m4a", ".wav"):
            if nombre.endswith(ext):
                extension = ext
                break
    if extension is None:
        raise HTTPException(status_code=400, detail="Formato de audio no soportado")

    contenido = await audio.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="El audio esta vacio")
    if len(contenido) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=400, detail="El audio supera el maximo de 25 MB")

    nota_id = str(uuid.uuid4())
    ruta = CARPETA_AUDIO / f"{nota_id}{extension}"
    ruta.write_bytes(contenido)

    organizacion = org if org and org not in ("todas", "personal", "externo") else None
    db.execute(
        text("""
            INSERT INTO notas_voz (id, usuario_id, organizacion_id, audio_path, duracion_seg, estado)
            VALUES (:id, :uid, :org, :ruta, :dur, 'pendiente')
        """),
        {"id": nota_id, "uid": uid, "org": organizacion, "ruta": str(ruta), "dur": duracion},
    )
    db.commit()

    transcripcion = None
    aviso = None
    if hay_transcriptor():
        try:
            transcripcion = transcribir(str(ruta))
            db.execute(
                text("""
                    UPDATE notas_voz SET transcripcion = :txt, estado = 'transcrita'
                    WHERE id = :id
                """),
                {"id": nota_id, "txt": transcripcion},
            )
            db.commit()
            print(f"[VOZ] Nota {nota_id} transcrita ({len(transcripcion)} caracteres)")
        except Exception as e:
            aviso = f"No se pudo transcribir automaticamente: {e}"
            print(f"[VOZ] Error transcribiendo {nota_id}: {e}")
    else:
        aviso = "Transcripcion automatica no configurada; escribela manualmente"

    return {
        "id": nota_id,
        "mensaje": "Audio guardado",
        "transcripcion": transcripcion,
        "aviso": aviso,
        "estado": "transcrita" if transcripcion else "pendiente",
    }


@router.post("/{nota_id}/retranscribir")
def retranscribir(
    nota_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Vuelve a transcribir el audio de una nota existente."""
    from transcriptor import transcribir

    fila = db.execute(
        text("SELECT audio_path FROM notas_voz WHERE id = :id AND usuario_id = :uid"),
        {"id": nota_id, "uid": uid},
    ).fetchone()
    if fila is None or not fila.audio_path:
        raise HTTPException(status_code=404, detail="Nota de voz no encontrada")

    try:
        texto = transcribir(fila.audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al transcribir: {e}")

    db.execute(
        text("UPDATE notas_voz SET transcripcion = :txt, estado = 'transcrita' WHERE id = :id"),
        {"id": nota_id, "txt": texto},
    )
    db.commit()
    return {"transcripcion": texto}


@router.get("/{nota_id}/audio")
def escuchar_audio(
    nota_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Devuelve el archivo de audio de una nota."""
    fila = db.execute(
        text("SELECT audio_path FROM notas_voz WHERE id = :id AND usuario_id = :uid"),
        {"id": nota_id, "uid": uid},
    ).fetchone()
    if fila is None or not fila.audio_path:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    ruta = Path(fila.audio_path)
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo de audio no encontrado")
    return FileResponse(ruta)


@router.put("/{nota_id}/transcripcion")
def guardar_transcripcion(
    nota_id: str,
    datos: Transcripcion,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Guarda o corrige la transcripcion de una nota."""
    existe = db.execute(
        text("SELECT id FROM notas_voz WHERE id = :id AND usuario_id = :uid"),
        {"id": nota_id, "uid": uid},
    ).fetchone()
    if existe is None:
        raise HTTPException(status_code=404, detail="Nota de voz no encontrada")
    if not datos.transcripcion.strip():
        raise HTTPException(status_code=400, detail="La transcripcion no puede estar vacia")

    db.execute(
        text("""
            UPDATE notas_voz SET transcripcion = :txt, estado = 'transcrita'
            WHERE id = :id AND usuario_id = :uid
        """),
        {"id": nota_id, "uid": uid, "txt": datos.transcripcion.strip()},
    )
    db.commit()
    return {"mensaje": "Transcripcion guardada"}


@router.post("/{nota_id}/analizar")
def analizar_nota(
    nota_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Analiza la transcripcion con Claude y resuelve coincidencias."""
    from generador_ia import analizar_nota_voz
    from coincidencias import buscar_coincidencia

    fila = db.execute(
        text("SELECT transcripcion FROM notas_voz WHERE id = :id AND usuario_id = :uid"),
        {"id": nota_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Nota de voz no encontrada")
    if not fila.transcripcion:
        raise HTTPException(status_code=400, detail="La nota aun no tiene transcripcion")

    contactos_bd = [
        {"id": str(f.id), "nombre": f.nombre}
        for f in db.execute(
            text("SELECT id, nombre FROM contactos WHERE usuario_id = :uid"), {"uid": uid}
        ).fetchall()
    ]
    empresas_bd = [
        {"id": str(f.id), "nombre": f.nombre}
        for f in db.execute(
            text("SELECT id, nombre FROM empresas WHERE usuario_id = :uid"), {"uid": uid}
        ).fetchall()
    ]

    try:
        analisis = analizar_nota_voz(
            fila.transcripcion,
            [c["nombre"] for c in contactos_bd],
            [e["nombre"] for e in empresas_bd],
        )
    except Exception as e:
        db.execute(
            text("UPDATE notas_voz SET estado = 'error' WHERE id = :id"), {"id": nota_id}
        )
        db.commit()
        raise HTTPException(status_code=500, detail=f"Error al analizar con IA: {e}")

    for c in analisis.get("contactos", []):
        existente, _ = buscar_coincidencia(c.get("nombre", ""), contactos_bd, umbral=0.8)
        if existente:
            c["id_existente"] = existente["id"]
            c["nombre_existente"] = existente["nombre"]
    for e in analisis.get("empresas", []):
        existente, _ = buscar_coincidencia(
            e.get("nombre", ""), empresas_bd, es_empresa=True, umbral=0.75
        )
        if existente:
            e["id_existente"] = existente["id"]
            e["nombre_existente"] = existente["nombre"]

    db.execute(
        text("""
            UPDATE notas_voz SET analisis = :an, estado = 'analizada'
            WHERE id = :id AND usuario_id = :uid
        """),
        {"id": nota_id, "uid": uid, "an": _json.dumps(analisis, ensure_ascii=False)},
    )
    db.commit()
    return analisis


@router.get("")
def listar_notas_voz(
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Historial de notas de voz del usuario."""
    filas = db.execute(
        text("""
            SELECT n.id, n.transcripcion, n.estado, n.duracion_seg, n.creada_en,
                   o.nombre AS organizacion
            FROM notas_voz n
            LEFT JOIN usuario_organizaciones o ON o.id = n.organizacion_id
            WHERE n.usuario_id = :uid
            ORDER BY n.creada_en DESC
            LIMIT 50
        """),
        {"uid": uid},
    ).fetchall()
    return [
        {
            "id": str(f.id),
            "transcripcion": (f.transcripcion or "")[:200],
            "estado": f.estado,
            "duracion_seg": f.duracion_seg,
            "organizacion": f.organizacion,
            "creada_en": str(f.creada_en),
        }
        for f in filas
    ]


@router.delete("/{nota_id}")
def eliminar_nota_voz(
    nota_id: str,
    db: Session = Depends(obtener_sesion),
    uid: str = Depends(usuario_actual),
):
    """Elimina una nota de voz y su audio."""
    fila = db.execute(
        text("SELECT audio_path FROM notas_voz WHERE id = :id AND usuario_id = :uid"),
        {"id": nota_id, "uid": uid},
    ).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Nota de voz no encontrada")
    if fila.audio_path:
        ruta = Path(fila.audio_path)
        if ruta.exists():
            ruta.unlink()
    db.execute(
        text("DELETE FROM notas_voz WHERE id = :id AND usuario_id = :uid"),
        {"id": nota_id, "uid": uid},
    )
    db.commit()
    return {"mensaje": "Nota de voz eliminada"}