-- ============================================================
-- Proyecto Papa — Modelo de datos (PostgreSQL)
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ------------------------------------------------------------
-- EMPRESAS
-- ------------------------------------------------------------
CREATE TABLE empresas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre          TEXT NOT NULL,
    nicho           TEXT,
    descripcion     TEXT,
    sitio_web       TEXT,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ------------------------------------------------------------
-- CONTACTOS
-- ------------------------------------------------------------
CREATE TABLE contactos (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre          TEXT NOT NULL,
    empresa_id      UUID REFERENCES empresas(id) ON DELETE SET NULL,
    cargo           TEXT,
    nicho           TEXT,
    telefono        TEXT,
    linkedin_url    TEXT,
    notas_generales TEXT,
    relacion_tipo   TEXT CHECK (relacion_tipo IN ('cliente','proveedor','socio','empresario','otro')),
    relacion_estado TEXT,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE contacto_emails (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contacto_id UUID NOT NULL REFERENCES contactos(id) ON DELETE CASCADE,
    email       TEXT NOT NULL,
    UNIQUE (email)
);
CREATE INDEX idx_contacto_emails_email ON contacto_emails (lower(email));

-- ------------------------------------------------------------
-- EVENTOS (Google Calendar)
-- ------------------------------------------------------------
CREATE TABLE eventos (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gcal_event_id       TEXT UNIQUE NOT NULL,
    titulo              TEXT NOT NULL,
    descripcion         TEXT,
    ubicacion           TEXT,
    inicio              TIMESTAMPTZ NOT NULL,
    fin                 TIMESTAMPTZ,
    link_reunion        TEXT,
    sincronizado_en     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_eventos_inicio ON eventos (inicio);

CREATE TABLE evento_asistentes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evento_id   UUID NOT NULL REFERENCES eventos(id) ON DELETE CASCADE,
    email       TEXT,
    nombre      TEXT,
    contacto_id UUID REFERENCES contactos(id) ON DELETE SET NULL,
    UNIQUE (evento_id, email)
);
CREATE INDEX idx_evento_asistentes_sin_match
    ON evento_asistentes (evento_id) WHERE contacto_id IS NULL;

-- ------------------------------------------------------------
-- INTERACCIONES
-- ------------------------------------------------------------
CREATE TABLE interacciones (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contacto_id     UUID NOT NULL REFERENCES contactos(id) ON DELETE CASCADE,
    evento_id       UUID REFERENCES eventos(id) ON DELETE SET NULL,
    tipo            TEXT NOT NULL CHECK (tipo IN ('reunion','llamada','email','nota','whatsapp','otro')),
    fecha           TIMESTAMPTZ NOT NULL DEFAULT now(),
    contenido_raw   TEXT NOT NULL,
    resumen_ia      TEXT,
    temas_pendientes JSONB,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_interacciones_contacto_fecha ON interacciones (contacto_id, fecha DESC);

-- ------------------------------------------------------------
-- DOCUMENTOS (Google Drive)
-- ------------------------------------------------------------
CREATE TABLE documentos (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gdrive_file_id  TEXT UNIQUE NOT NULL,
    nombre          TEXT NOT NULL,
    mime_type       TEXT,
    empresa_id      UUID REFERENCES empresas(id) ON DELETE SET NULL,
    contacto_id     UUID REFERENCES contactos(id) ON DELETE SET NULL,
    texto_extraido  TEXT,
    resumen_ia      TEXT,
    modificado_en   TIMESTAMPTZ,
    sincronizado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_documentos_empresa ON documentos (empresa_id);
CREATE INDEX idx_documentos_texto_trgm ON documentos USING gin (texto_extraido gin_trgm_ops);

-- ------------------------------------------------------------
-- LINKS DE LINKEDIN
-- ------------------------------------------------------------
CREATE TABLE links_linkedin (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url             TEXT NOT NULL,
    contacto_id     UUID REFERENCES contactos(id) ON DELETE SET NULL,
    es_propio       BOOLEAN NOT NULL DEFAULT false,
    texto_extraido  TEXT,
    resumen_ia      TEXT,
    guardado_en     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (url)
);
CREATE INDEX idx_links_contacto ON links_linkedin (contacto_id);

-- ------------------------------------------------------------
-- NOTICIAS POR NICHO
-- ------------------------------------------------------------
CREATE TABLE noticias (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nicho           TEXT NOT NULL,
    titulo          TEXT NOT NULL,
    fuente          TEXT,
    url             TEXT UNIQUE,
    publicada_en    TIMESTAMPTZ,
    resumen_ia      TEXT,
    recolectada_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_noticias_nicho_fecha ON noticias (nicho, publicada_en DESC);

-- ------------------------------------------------------------
-- BRIEFS GENERADOS
-- ------------------------------------------------------------
CREATE TABLE briefs_generados (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo            TEXT NOT NULL CHECK (tipo IN ('brief_diario','ficha_reunion')),
    fecha           DATE NOT NULL,
    evento_id       UUID REFERENCES eventos(id) ON DELETE CASCADE,
    contenido       JSONB NOT NULL,
    modelo_usado    TEXT,
    generado_en     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tipo, fecha, evento_id)
);
CREATE INDEX idx_briefs_fecha ON briefs_generados (fecha DESC);

-- ------------------------------------------------------------
-- JOBS DE SINCRONIZACIÓN
-- ------------------------------------------------------------
CREATE TABLE sync_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo            TEXT NOT NULL,
    estado          TEXT NOT NULL DEFAULT 'pendiente'
                    CHECK (estado IN ('pendiente','corriendo','ok','error')),
    detalle_error   TEXT,
    inicio          TIMESTAMPTZ,
    fin             TIMESTAMPTZ,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ------------------------------------------------------------
-- Trigger para actualizado_en
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION touch_actualizado_en() RETURNS trigger AS $$
BEGIN
    NEW.actualizado_en = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_empresas_touch  BEFORE UPDATE ON empresas  FOR EACH ROW EXECUTE FUNCTION touch_actualizado_en();
CREATE TRIGGER trg_contactos_touch BEFORE UPDATE ON contactos FOR EACH ROW EXECUTE FUNCTION touch_actualizado_en();