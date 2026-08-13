"""Migra las claves del .env a hashes cifrados en la base de datos.

Ejecutar una sola vez:  python migrar_claves.py
"""
import os

import bcrypt
from dotenv import load_dotenv
from sqlalchemy import text

from database import SesionLocal

load_dotenv()


def cifrar(clave: str) -> str:
    """Genera el hash bcrypt de una clave."""
    return bcrypt.hashpw(clave.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def main():
    lista = os.getenv("APP_USUARIOS", "").strip()
    if not lista:
        print("No hay APP_USUARIOS en el .env")
        return

    db = SesionLocal()
    migrados = 0
    try:
        for par in lista.split(","):
            if ":" not in par:
                continue
            usuario, clave = par.split(":", 1)
            usuario = usuario.strip().lower()
            clave = clave.strip()
            if not usuario or not clave:
                continue

            existe = db.execute(
                text("SELECT id FROM usuarios WHERE username = :u"), {"u": usuario}
            ).fetchone()

            hash_clave = cifrar(clave)
            if existe:
                db.execute(
                    text("UPDATE usuarios SET password_hash = :h WHERE username = :u"),
                    {"h": hash_clave, "u": usuario},
                )
                print(f"  Clave cifrada para: {usuario}")
            else:
                db.execute(
                    text("""
                        INSERT INTO usuarios (username, nombre_visible, password_hash)
                        VALUES (:u, :n, :h)
                    """),
                    {"u": usuario, "n": usuario.capitalize(), "h": hash_clave},
                )
                print(f"  Usuario creado con clave cifrada: {usuario}")
            migrados += 1
        db.commit()
        print(f"\nListo: {migrados} usuario(s) migrados.")
        print("Ahora puedes borrar la linea APP_USUARIOS del .env.")
    finally:
        db.close()


if __name__ == "__main__":
    main()