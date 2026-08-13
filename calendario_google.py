"""Conexion y sincronizacion con Google Calendar."""
import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

PERMISOS = ["https://www.googleapis.com/auth/calendar.readonly"]
ARCHIVO_CREDENCIALES = "credenciales_google.json"
ARCHIVO_TOKEN = "token_google.json"


def obtener_servicio():
    """Devuelve el cliente de Calendar, pidiendo autorizacion la primera vez."""
    creds = None
    if os.path.exists(ARCHIVO_TOKEN):
        creds = Credentials.from_authorized_user_file(ARCHIVO_TOKEN, PERMISOS)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(ARCHIVO_CREDENCIALES, PERMISOS)
            creds = flow.run_local_server(port=0)
        with open(ARCHIVO_TOKEN, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def traer_eventos(dias: int = 7):
    """Trae los eventos de los proximos N dias del calendario principal."""
    servicio = obtener_servicio()
    ahora = datetime.datetime.now(datetime.timezone.utc)
    hasta = ahora + datetime.timedelta(days=dias)

    resultado = servicio.events().list(
        calendarId="primary",
        timeMin=ahora.isoformat(),
        timeMax=hasta.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=100,
    ).execute()

    eventos = []
    for ev in resultado.get("items", []):
        inicio = ev.get("start", {}).get("dateTime") or ev.get("start", {}).get("date")
        fin = ev.get("end", {}).get("dateTime") or ev.get("end", {}).get("date")
        asistentes = [
            {"email": a.get("email"), "nombre": a.get("displayName")}
            for a in ev.get("attendees", [])
            if not a.get("self")
        ]
        eventos.append({
            "gcal_event_id": ev["id"],
            "titulo": ev.get("summary", "(sin titulo)"),
            "descripcion": ev.get("description"),
            "ubicacion": ev.get("location"),
            "inicio": inicio,
            "fin": fin,
            "link_reunion": ev.get("hangoutLink"),
            "asistentes": asistentes,
        })
    return eventos