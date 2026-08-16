"""Autenticacion multiusuario con claves cifradas en la base de datos."""
import os

from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from passlib.hash import bcrypt
from sqlalchemy import text

from database import SesionLocal

load_dotenv()

SECRETO = os.getenv("APP_SECRETO_SESION", "secreto-por-defecto-cambiar")
DURACION_SESION = 60 * 60 * 24 * 30  # 30 dias

firmador = URLSafeTimedSerializer(SECRETO)

RUTAS_LIBRES = {"/login", "/entrar", "/salud", "/favicon.ico"}


def validar_credenciales(usuario: str, clave: str):
    """Valida contra el hash guardado en la base de datos.

    Devuelve (username, usuario_id) si son correctas, o None.
    """
    nombre = (usuario or "").strip().lower()
    if not nombre or not clave:
        return None

    db = SesionLocal()
    try:
        fila = db.execute(
            text("""
                SELECT id, username, password_hash, activo
                FROM usuarios WHERE username = :u
            """),
            {"u": nombre},
        ).fetchone()
        if fila is None or not fila.activo or not fila.password_hash:
            return None
        try:
            if not bcrypt.verify(clave, fila.password_hash):
                return None
        except Exception:
            return None
        return fila.username, str(fila.id)
    finally:
        db.close()


def cambiar_clave(usuario_id: str, clave_nueva: str) -> bool:
    """Actualiza la clave de un usuario."""
    if not clave_nueva or len(clave_nueva) < 6:
        return False
    db = SesionLocal()
    try:
        db.execute(
            text("UPDATE usuarios SET password_hash = :h WHERE id = :id"),
            {"h": bcrypt.hash(clave_nueva), "id": usuario_id},
        )
        db.commit()
        return True
    finally:
        db.close()


def usuario_existe(username: str) -> bool:
    db = SesionLocal()
    try:
        fila = db.execute(
            text("SELECT id FROM usuarios WHERE username = :u"),
            {"u": username.strip().lower()},
        ).fetchone()
        return fila is not None
    finally:
        db.close()


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


def nombre_usuario_actual(request: Request):
    datos = _leer_cookie(request)
    return datos.get("usuario") if datos else None


PAGINA_LOGIN = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Integra Life</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
         background: #F4F6F9; min-height: 100vh; display: flex;
         align-items: center; justify-content: center; padding: 1rem; }
  .caja { background: white; border: 1px solid #E3E7EE; border-top: 4px solid #26529E;
          border-radius: 3px; padding: 2.2rem; width: 100%; max-width: 380px;
          box-shadow: 0 2px 12px rgba(54,63,76,.10); text-align: center; }
  .logo { width: 54px; height: 54px; border-radius: 2px; margin: 0 auto 1rem;
          background: #26529E; display: flex; align-items: center;
          justify-content: center; color: white; font-weight: 700; font-size: 1.3rem; }
  h1 { font-size: 1.25rem; color: #26529E; margin-bottom: .2rem; }
  .sub { color: #7B8494; font-size: .85rem; margin-bottom: 1.6rem; }
  input { width: 100%; border: 1px solid #D8DEE8; border-radius: 3px;
          padding: .75rem .9rem; font-size: .95rem; margin-bottom: .8rem;
          outline: none; font-family: inherit; }
  input:focus { border-color: #26529E; }
  button { width: 100%; border: none; border-radius: 3px; padding: .8rem;
           font-size: .95rem; font-weight: 700; color: white; cursor: pointer;
           background: #26529E; }
  button:hover { background: #1d4080; }
  .error { color: #B03A3A; font-size: .85rem; margin-top: .8rem; }
</style>
</head>
<body>
<div class="caja">
  <div class="logo">IL</div>
  <h1>Integra Life</h1>
  <div class="sub">tu memoria ejecutiva</div>
  <form method="post" action="/entrar">
    <input type="text" name="usuario" placeholder="Usuario" autocomplete="username" required autofocus>
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