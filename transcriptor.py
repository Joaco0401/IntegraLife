"""Transcripcion de audio con la API de OpenAI (Whisper)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_clave = os.getenv("OPENAI_API_KEY")
cliente = OpenAI(api_key=_clave) if _clave else None

MODELO_TRANSCRIPCION = "whisper-1"
MAX_BYTES = 25_000_000


def hay_transcriptor() -> bool:
    """Indica si esta configurada la clave de OpenAI."""
    return cliente is not None


def transcribir(ruta_audio: str) -> str:
    """Envia el audio a Whisper y devuelve el texto transcrito."""
    if cliente is None:
        raise RuntimeError(
            "Falta OPENAI_API_KEY en el archivo .env para transcribir automaticamente"
        )

    ruta = Path(ruta_audio)
    if not ruta.exists():
        raise FileNotFoundError("No se encontro el archivo de audio")
    if ruta.stat().st_size > MAX_BYTES:
        raise ValueError("El audio supera el maximo de 25 MB que acepta el transcriptor")

    with open(ruta, "rb") as f:
        respuesta = cliente.audio.transcriptions.create(
            model=MODELO_TRANSCRIPCION,
            file=f,
            language="es",
            prompt=(
                "Nota de voz de un empresario chileno sobre reuniones de negocios. "
                "Puede mencionar nombres de personas y empresas."
            ),
        )
    return (respuesta.text or "").strip()