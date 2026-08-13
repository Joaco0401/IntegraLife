"""Generador de resumenes y extraccion de datos con Claude."""
import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODELO = "claude-sonnet-4-6"


def _limpiar(texto: str) -> str:
    return texto.strip().replace("```json", "").replace("```", "").strip()


def _rescatar_json_truncado(texto: str):
    """Si la respuesta quedo cortada, recupera los objetos completos."""
    resultado = {"empresas": [], "contactos": [], "eventos": []}
    for clave in resultado:
        inicio = texto.find('"' + clave + '"')
        if inicio == -1:
            continue
        corchete = texto.find("[", inicio)
        if corchete == -1:
            continue
        profundidad = 0
        objetos = []
        actual = ""
        for ch in texto[corchete + 1:]:
            if ch == "{":
                profundidad += 1
            if profundidad > 0:
                actual += ch
            if ch == "}":
                profundidad -= 1
                if profundidad == 0:
                    objetos.append(actual)
                    actual = ""
            if ch == "]" and profundidad == 0:
                break
        for obj in objetos:
            try:
                resultado[clave].append(json.loads(obj))
            except json.JSONDecodeError:
                pass
    return resultado


def _extraer_json(texto: str):
    texto = _limpiar(texto)
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        rescatado = _rescatar_json_truncado(texto)
        if any(rescatado.values()):
            print("[IA] Respuesta truncada: se rescataron los registros completos")
            return rescatado
        raise


def resumir_interaccion(nombre_contacto: str, tipo: str, contenido: str) -> dict:
    """Lee una interaccion y devuelve resumen + temas pendientes en JSON."""
    prompt = f"""Eres el asistente ejecutivo de Rodrigo, un empresario muy ocupado.
Acaba de registrarse esta interaccion con su contacto {nombre_contacto}:

Tipo: {tipo}
Contenido: {contenido}

Genera un JSON con exactamente esta estructura (responde SOLO el JSON, sin
explicaciones ni markdown):
{{
  "resumen": "resumen de 1-2 frases de lo esencial, en tono directo",
  "temas_pendientes": ["lista de compromisos o tareas que quedaron abiertas"],
  "datos_clave": ["hechos importantes para recordar a futuro"]
}}

Importante sobre temas_pendientes: incluye TODAS las tareas o compromisos
mencionados, indicando el responsable cuando corresponda. Por ejemplo:
"Enviar cotizacion (responsable: Rodrigo)" o "Confirmar fecha de visita
(responsable: {nombre_contacto})". Manten cada tema en una sola linea corta."""

    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    texto = _limpiar(respuesta.content[0].text)
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"resumen": texto[:400], "temas_pendientes": [], "datos_clave": []}


def extraer_entidades(texto_archivo: str) -> dict:
    """Extrae contactos, empresas, notas, tareas por responsable y eventos."""
    prompt = f"""Eres el asistente de datos de una plataforma CRM.
Analiza el siguiente contenido de un archivo y extrae:
1. Todas las EMPRESAS (organizaciones) mencionadas.
2. Todos los CONTACTOS (personas) mencionados, INCLUYENDO a quienes solo
   aparecen como responsables de una tarea.
3. Las NOTAS de cada persona: contexto, acuerdos, y las TAREAS de las que
   esa persona es responsable.
4. Los EVENTOS con fecha (reuniones, hitos, plazos, recordatorios).

CONTENIDO DEL ARCHIVO:
{texto_archivo[:15000]}

La fecha de hoy es 2026-08-13 (formato AAAA-MM-DD). Usa esto para resolver
fechas relativas como "el viernes" o "la proxima semana".

IMPORTANTE sobre la columna o campo "Organizacion":
Si el archivo tiene una columna llamada "Organizacion" (o similar), ese valor
NO es la empresa donde trabaja la persona: es el contexto del usuario que
importa. Colocalo en "organizacion_detectada", y usa la columna "Empresa"
para la empresa donde trabaja la persona.

Responde SOLO un JSON valido con esta estructura exacta, sin explicaciones
ni markdown:
{{
  "organizacion_detectada": "nombre de la organizacion del archivo o null",
  "empresas": [
    {{"nombre": "...", "nicho": "... o null", "descripcion": "... o null"}}
  ],
  "contactos": [
    {{"nombre": "...", "cargo": "... o null", "email": "... o null",
      "telefono": "... o null", "empresa_nombre": "empresa donde trabaja o null",
      "relacion_tipo": "cliente, proveedor, socio, empresario, otro, o null",
      "notas": "contexto y tareas a su cargo, o null"}}
  ],
  "eventos": [
    {{"titulo": "...", "fecha": "AAAA-MM-DD o null", "hora": "HH:MM o null",
      "lugar": "... o null", "notas": "... o null",
      "contacto_nombre": "contacto involucrado o null"}}
  ]
}}

Reglas de formato (IMPORTANTES para que la respuesta no se corte):
- SE BREVE. Cada campo "notas" maximo 250 caracteres.
- Cada "descripcion" maximo 120 caracteres.
- No uses saltos de linea dentro de los textos.
- Maximo 40 contactos, 20 empresas y 20 eventos.

Reglas de contenido:
- Si un dato no aparece, usa null. NO inventes datos.
- Si una tarea tiene responsable, DEBE aparecer en las notas de ese contacto.
- Ignora las filas de ejemplo o de ayuda de las plantillas.
- Si no hay elementos de alguna categoria, devuelve lista vacia."""

    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    datos = _extraer_json(respuesta.content[0].text)
    return {
        "organizacion_detectada": datos.get("organizacion_detectada"),
        "empresas": datos.get("empresas", []),
        "contactos": datos.get("contactos", []),
        "eventos": datos.get("eventos", []),
    }


def analizar_nota_voz(transcripcion: str, contactos_conocidos: list, empresas_conocidas: list) -> dict:
    """Analiza la transcripcion de una nota de voz y distribuye la informacion."""
    lista_contactos = ", ".join(contactos_conocidos[:80]) or "(ninguno registrado aun)"
    lista_empresas = ", ".join(empresas_conocidas[:50]) or "(ninguna registrada aun)"

    prompt = f"""Eres el asistente ejecutivo de un empresario. Acaba de salir de
una reunion y dicto esta nota de voz. Tu trabajo es ordenar la informacion y
repartirla donde corresponde.

TRANSCRIPCION:
{transcripcion[:12000]}

CONTACTOS YA REGISTRADOS EN EL SISTEMA:
{lista_contactos}

EMPRESAS YA REGISTRADAS EN EL SISTEMA:
{lista_empresas}

La fecha de hoy es 2026-08-13 (formato AAAA-MM-DD). Usa esto para resolver
fechas relativas como "el viernes" o "la proxima semana".

Responde SOLO un JSON valido con esta estructura exacta, sin explicaciones
ni markdown:
{{
  "resumen_general": "2-3 frases con lo esencial de la nota",
  "contactos": [
    {{"nombre": "nombre de la persona",
      "es_nuevo": true,
      "empresa_nombre": "empresa donde trabaja o null",
      "cargo": "cargo si se menciona o null",
      "resumen": "que se converso con esta persona, 1-2 frases",
      "temas_pendientes": ["compromisos concretos, indicando responsable"]}}
  ],
  "empresas": [
    {{"nombre": "nombre de la empresa",
      "es_nueva": true,
      "nicho": "rubro si se menciona o null",
      "resumen": "informacion relevante sobre la empresa surgida en la conversacion",
      "datos_clave": ["hechos del negocio: planes, cifras, decisiones, contexto"]}}
  ],
  "eventos": [
    {{"titulo": "...", "fecha": "AAAA-MM-DD o null", "hora": "HH:MM o null",
      "contacto_nombre": "persona involucrada o null", "notas": "... o null"}}
  ]
}}

Reglas:
- Si un nombre se parece a uno ya registrado, usa EXACTAMENTE el nombre registrado
  y marca es_nuevo/es_nueva como false.
- La informacion de negocio (planes, cifras, decisiones estrategicas) va en la
  empresa. Lo relacional y los compromisos van en el contacto.
- Si la nota menciona una persona pero no su empresa, deja empresa_nombre en null.
- SE BREVE: cada resumen maximo 250 caracteres, sin saltos de linea.
- No inventes datos que no esten en la transcripcion.
- Si no hay elementos de alguna categoria, devuelve lista vacia."""

    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    datos = _extraer_json(respuesta.content[0].text)
    return {
        "resumen_general": datos.get("resumen_general"),
        "contactos": datos.get("contactos", []),
        "empresas": datos.get("empresas", []),
        "eventos": datos.get("eventos", []),
    }


def generar_brief_diario(nombre_usuario: str, fecha_texto: str, eventos: list,
                         pendientes: list, organizaciones: list) -> dict:
    """Escribe el resumen ejecutivo del dia."""
    if not eventos and not pendientes:
        return {
            "saludo": f"Buenos dias, {nombre_usuario}",
            "resumen": "No tienes eventos ni pendientes registrados para hoy.",
            "puntos_clave": [],
            "sugerencias": [],
        }

    texto_eventos = "\n".join(
        f"- {e['hora']} · {e['titulo']}"
        f"{' en ' + e['ubicacion'] if e.get('ubicacion') else ''}"
        f"{' con ' + ', '.join(e['asistentes']) if e.get('asistentes') else ''}"
        f"{' | contexto: ' + e['contexto'] if e.get('contexto') else ''}"
        for e in eventos
    ) or "(sin eventos agendados)"

    texto_pendientes = "\n".join(
        f"- {p['texto']} (con {p['contacto']}"
        f"{', ' + p['empresa'] if p.get('empresa') else ''}"
        f", registrado hace {p['dias']} dias)"
        for p in pendientes[:20]
    ) or "(sin pendientes abiertos)"

    texto_orgs = ", ".join(organizaciones) or "sin organizaciones definidas"

    prompt = f"""Eres el asistente ejecutivo de {nombre_usuario}, un empresario
con poco tiempo que necesita llegar preparado a su dia.

Hoy es {fecha_texto}. Trabaja en: {texto_orgs}.

AGENDA DE HOY:
{texto_eventos}

PENDIENTES ABIERTOS:
{texto_pendientes}

Escribe su brief matutino. Responde SOLO un JSON valido con esta estructura,
sin explicaciones ni markdown:
{{
  "saludo": "saludo breve y personal",
  "resumen": "2-4 frases con como se ve el dia: cuantas reuniones, cuales son
              las mas importantes y por que",
  "puntos_clave": ["lo que no puede olvidar hoy, maximo 5, en frases cortas
                    y accionables"],
  "sugerencias": ["recomendaciones concretas: a quien retomar, que preparar
                   antes de una reunion, que compromiso esta demorado. Maximo 3"]
}}

Reglas:
- Tono directo y profesional, sin adornos ni frases de relleno.
- Menciona nombres propios de personas y empresas cuando aporte.
- Si un pendiente lleva mucho tiempo abierto, senalalo.
- Si una reunion de hoy tiene compromisos pendientes con esa persona, avisalo:
  es lo mas valioso del brief.
- Habla en segunda persona (tu tienes, deberias).
- Se breve: cada punto maximo 140 caracteres."""

    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    datos = _extraer_json(respuesta.content[0].text)
    return {
        "saludo": datos.get("saludo", f"Buenos dias, {nombre_usuario}"),
        "resumen": datos.get("resumen", ""),
        "puntos_clave": datos.get("puntos_clave", []),
        "sugerencias": datos.get("sugerencias", []),
    }