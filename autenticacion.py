"""Autenticacion multiusuario con sesiones por cookie para Integra Life."""
import os

from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import text

from database import SesionLocal

load_dotenv()

SECRETO = os.getenv("APP_SECRETO_SESION", "secreto-por-defecto-cambiar")
DURACION_SESION = 60 * 60 * 24 * 30  # 30 dias en segundos

firmador = URLSafeTimedSerializer(SECRETO)

RUTAS_LIBRES = {"/login", "/entrar", "/salud", "/favicon.ico"}


def _cargar_usuarios() -> dict:
    """Lee los usuarios desde APP_USUARIOS (formato usuario:clave,usuario:clave)."""
    usuarios = {}
    lista = os.getenv("APP_USUARIOS", "").strip()
    if lista:
        for par in lista.split(","):
            if ":" in par:
                nombre, clave = par.split(":", 1)
                nombre = nombre.strip().lower()
                clave = clave.strip()
                if nombre and clave:
                    usuarios[nombre] = clave
    if not usuarios:
        nombre = os.getenv("APP_USUARIO", "").strip().lower()
        clave = os.getenv("APP_CLAVE", "").strip()
        if nombre and clave:
            usuarios[nombre] = clave
    return usuarios


USUARIOS = _cargar_usuarios()


def buscar_usuario_id(username: str) -> str | None:
    """Obtiene el id interno del usuario desde la base de datos."""
    db = SesionLocal()
    try:
        fila = db.execute(
            text("SELECT id FROM usuarios WHERE username = :u"),
            {"u": username.lower()},
        ).fetchone()
        return str(fila.id) if fila else None
    finally:
        db.close()


def validar_credenciales(usuario: str, clave: str):
    """Devuelve (username, usuario_id) si las credenciales son correctas."""
    nombre = (usuario or "").strip().lower()
    esperada = USUARIOS.get(nombre)
    if not esperada or clave != esperada:
        return None
    uid = buscar_usuario_id(nombre)
    if not uid:
        return None
    return nombre, uid


def crear_cookie_sesion(username: str, usuario_id: str) -> str:
    return firmador.dumps({"usuario": username, "usuario_id": usuario_id})


def _leer_cookie(request: Request):
    token = request.cookies.get("sesion_il")
    if not token:
        return None
    try:
        return firmador.loads(token, max_age=DURACION_SESION)
    except (BadSignature, SignatureExpired):
        return None


def sesion_valida(request: Request) -> bool:
    datos = _leer_cookie(request)
    return bool(datos and datos.get("usuario_id"))


def usuario_actual(request: Request) -> str:
    """Dependencia de FastAPI: entrega el usuario_id de quien esta logueado."""
    datos = _leer_cookie(request)
    if not datos or not datos.get("usuario_id"):
        raise HTTPException(status_code=401, detail="Sesion no valida")
    return datos["usuario_id"]


def nombre_usuario_actual(request: Request) -> str | None:
    datos = _leer_cookie(request)
    return datos.get("usuario") if datos else None


PAGINA_LOGIN = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Integra Life — Ingresar</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, -apple-system, sans-serif;
         background: linear-gradient(160deg, #eef4ff 0%, #f6f0fa 50%, #fff4ec 100%);
         min-height: 100vh; display: flex; align-items: center; justify-content: center;
         padding: 1rem; }
  .caja { background: white; border-radius: 20px; padding: 2.2rem; width: 100%;
          max-width: 380px; box-shadow: 0 20px 60px rgba(35,41,70,.18); text-align: center; }
  .logo { width: 56px; height: 56px; border-radius: 16px; margin: 0 auto 1rem;
          background: linear-gradient(135deg, #5b6cff, #9b5bff);
          display: flex; align-items: center; justify-content: center;
          color: white; font-weight: 800; font-size: 1.4rem;
          box-shadow: 0 6px 18px rgba(91,108,255,.35); }
  h1 { font-size: 1.3rem; color: #232946; margin-bottom: .2rem; }
  .sub { color: #8a90b8; font-size: .85rem; margin-bottom: 1.6rem; }
  input { width: 100%; border: 1px solid #dfe3f4; border-radius: 12px;
          padding: .75rem .9rem; font-size: .95rem; margin-bottom: .8rem;
          outline: none; font-family: inherit; }
  input:focus { border-color: #5b6cff; }
  button { width: 100%; border: none; border-radius: 12px; padding: .8rem;
           font-size: .95rem; font-weight: 700; color: white; cursor: pointer;
           background: linear-gradient(135deg, #5b6cff, #9b5bff);
           box-shadow: 0 6px 18px rgba(91,108,255,.35); }
  .error { color: #d84343; font-size: .85rem; margin-top: .8rem; }
</style>
</head>
<body>
<div class="caja">
  <div class="logo">IL</div>
  <h1>Integra Life</h1>
  <div class="sub">tu memoria ejecutiva</div>
  <form method="post" action="/entrar">
    <input type="text" name="usuario" placeholder="Usuario" autocomplete="username" required>
    <input type="password" name="clave" placeholder="Contrase\u00f1a" autocomplete="current-password" required>
    <button type="submit">Ingresar</button>
    __ERROR__
  </form>
</div>
</body>
</html>"""


def pagina_login(con_error: bool = False) -> HTMLResponse:
    html = PAGINA_LOGIN.replace(
        "__ERROR__",
        '<div class="error">Usuario o contrase\u00f1a incorrectos</div>' if con_error else "",
    )
    return HTMLResponse(html)