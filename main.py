"""Integra Life — Backend principal."""
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import SesionLocal, obtener_sesion
from autenticacion import (
    RUTAS_LIBRES, validar_credenciales, nombre_usuario_actual,
    crear_cookie_sesion, sesion_valida, pagina_login,
)
import rutas_empresas
import rutas_contactos
import rutas_interacciones
import rutas_panel
import rutas_calendario
import rutas_importar
import rutas_organizacion
import rutas_perfil
import rutas_voz
import rutas_hoy

DESCRIPCION = """
**Integra Life** — tu memoria ejecutiva.

Plataforma de gestión de relaciones con inteligencia artificial.

👉 Para el uso diario, visita el [Panel visual](/panel).
"""

ETIQUETAS = [
    {"name": "Panel", "description": "Interfaz visual de la plataforma."},
    {"name": "Hoy", "description": "Panorama del día: agenda, pendientes y relaciones."},
    {"name": "Contactos", "description": "Personas con las que te relacionas."},
    {"name": "Empresas", "description": "Organizaciones de tus contactos."},
    {"name": "Interacciones", "description": "Notas con resumen automático de Claude."},
    {"name": "Calendario", "description": "Sincronización con Google Calendar."},
    {"name": "Importar", "description": "Carga de datos desde archivos."},
    {"name": "Notas de voz", "description": "Dictados que se convierten en contexto de contactos y empresas."},
    {"name": "Organizaciones", "description": "Organizaciones propias y tareas consolidadas."},
    {"name": "Perfil", "description": "Datos del usuario logueado."},
    {"name": "Acceso", "description": "Login y cierre de sesión."},
]


def sincronizar_calendario_automatico():
    """Job periodico: sincroniza el calendario de Google al usuario rodrigo.

    Respeta los eventos que el usuario elimino (tabla eventos_ocultos).
    """
    from rutas_calendario import sincronizar_para_usuario

    db = SesionLocal()
    try:
        usuario = db.execute(
            text("SELECT id FROM usuarios WHERE username = 'rodrigo'")
        ).fetchone()
        if usuario is None:
            print("[CAL] No existe el usuario rodrigo; se omite la sincronizacion")
            return
        guardados = sincronizar_para_usuario(db, str(usuario.id))
        print(f"[CAL] Sincronizacion automatica: {guardados} eventos")
    except Exception as e:
        print(f"[CAL] Error en sincronizacion automatica: {e}")
    finally:
        db.close()


@asynccontextmanager
async def ciclo_vida(app: FastAPI):
    programador = BackgroundScheduler()
    programador.add_job(sincronizar_calendario_automatico, "interval", minutes=5)
    programador.start()
    sincronizar_calendario_automatico()
    yield
    programador.shutdown()


app = FastAPI(
    title="Integra Life",
    version="1.0.0",
    description=DESCRIPCION,
    openapi_tags=ETIQUETAS,
    lifespan=ciclo_vida,
    swagger_ui_parameters={
        "docExpansion": "list",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
    },
)


@app.middleware("http")
async def proteger_rutas(request: Request, call_next):
    ruta = request.url.path
    if ruta in RUTAS_LIBRES or sesion_valida(request):
        return await call_next(request)
    return RedirectResponse("/login", status_code=302)


@app.get("/login", tags=["Acceso"], summary="Pantalla de ingreso")
def login():
    return pagina_login()


@app.post("/entrar", tags=["Acceso"], summary="Validar credenciales")
def entrar(usuario: str = Form(...), clave: str = Form(...)):
    resultado = validar_credenciales(usuario, clave)
    if resultado:
        nombre, uid = resultado
        respuesta = RedirectResponse("/panel", status_code=302)
        respuesta.set_cookie(
            "sesion_il",
            crear_cookie_sesion(nombre, uid),
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            samesite="lax",
        )
        return respuesta
    return pagina_login(con_error=True)


@app.get("/salir", tags=["Acceso"], summary="Cerrar sesión")
def salir():
    respuesta = RedirectResponse("/login", status_code=302)
    respuesta.delete_cookie("sesion_il")
    return respuesta


@app.get("/quien-soy", tags=["Acceso"], summary="Usuario conectado")
def quien_soy(request: Request):
    """Devuelve el nombre del usuario con sesion activa."""
    return {"usuario": nombre_usuario_actual(request)}


app.include_router(rutas_panel.router)
app.include_router(rutas_hoy.router)
app.include_router(rutas_contactos.router)
app.include_router(rutas_empresas.router)
app.include_router(rutas_interacciones.router)
app.include_router(rutas_calendario.router)
app.include_router(rutas_importar.router)
app.include_router(rutas_organizacion.router)
app.include_router(rutas_perfil.router)
app.include_router(rutas_voz.router)


@app.get("/", tags=["Panel"], summary="Inicio")
def raiz():
    return RedirectResponse("/panel", status_code=302)


@app.get("/salud", tags=["Panel"], summary="Chequeo de salud")
def salud(db: Session = Depends(obtener_sesion)):
    """Verifica que el servidor y la base de datos estén operativos."""
    resultado = db.execute(text("SELECT count(*) FROM contactos")).scalar()
    return {
        "servidor": "ok",
        "base_de_datos": "ok",
        "contactos_registrados": resultado,
    }