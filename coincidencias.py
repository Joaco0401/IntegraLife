"""Normalizacion y busqueda de coincidencias para evitar duplicados."""
import re
import unicodedata


def normalizar(texto):
    """Deja un texto comparable: sin tildes, apostrofes, puntos ni mayusculas.

    Ejemplos:
      "John O'Ryan Surveyors"  -> "john oryan surveyors"
      "John ORyan Surveyors"   -> "john oryan surveyors"
      "JOHN O RYAN SURVEYORS." -> "john oryan surveyors"
    """
    if not texto:
        return ""
    t = unicodedata.normalize("NFD", str(texto))
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    t = t.lower()
    t = re.sub(r"[\u0027\u2018\u2019\u0060\u00b4\"\.,;:_\-()]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


PALABRAS_VACIAS = {
    "spa", "sa", "ltda", "limitada", "eirl", "srl", "inc", "llc",
    "sociedad", "anonima", "cia", "compania", "the", "de", "del", "la", "y",
}


def clave_empresa(nombre):
    """Normaliza un nombre de empresa quitando sufijos societarios."""
    base = normalizar(nombre)
    if not base:
        return ""
    palabras = [p for p in base.split() if p not in PALABRAS_VACIAS]
    return " ".join(palabras) if palabras else base


def similitud(a, b):
    """Similitud simple entre dos textos ya normalizados (0 a 1)."""
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    pa, pb = set(a.split()), set(b.split())
    if not pa or not pb:
        return 0.0
    comunes = len(pa & pb)
    return comunes / max(len(pa), len(pb))


def buscar_coincidencia(nombre, candidatos, campo="nombre",
                        es_empresa=False, umbral=0.75):
    """Busca el candidato mas parecido a un nombre.

    candidatos: lista de dicts con al menos {id, <campo>}
    Devuelve (candidato, puntaje) o (None, puntaje) si nada supera el umbral.
    """
    fn = clave_empresa if es_empresa else normalizar
    objetivo = fn(nombre)
    if not objetivo:
        return None, 0.0

    mejor = None
    mejor_puntaje = 0.0
    for c in candidatos:
        puntaje = similitud(objetivo, fn(c.get(campo)))
        if puntaje > mejor_puntaje:
            mejor = c
            mejor_puntaje = puntaje

    if mejor_puntaje >= umbral:
        return mejor, mejor_puntaje
    return None, mejor_puntaje