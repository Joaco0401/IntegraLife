-- ============================================================
-- Integra Life — Organizaciones del usuario y contexto de contactos
-- ============================================================

-- Organizaciones en las que trabaja cada usuario
CREATE TABLE IF NOT EXISTS usuario_organizaciones (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id  UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre      TEXT NOT NULL,
    mi_cargo    TEXT,
    creado_en   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (usuario_id, nombre)
);
CREATE INDEX IF NOT EXISTS idx_org_usuario ON usuario_organizaciones (usuario_id);

-- Contexto: en cual de mis organizaciones se relaciona este contacto
ALTER TABLE contactos ADD COLUMN IF NOT EXISTS organizacion_id UUID
    REFERENCES usuario_organizaciones(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_contactos_org ON contactos (usuario_id, organizacion_id);

-- Contexto tambien en eventos, para filtrar la agenda
ALTER TABLE eventos ADD COLUMN IF NOT EXISTS organizacion_id UUID
    REFERENCES usuario_organizaciones(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_eventos_org ON eventos (usuario_id, organizacion_id);

-- Se elimina la empresa propia unica del esquema anterior
ALTER TABLE usuarios DROP COLUMN IF EXISTS empresa_propia_id;