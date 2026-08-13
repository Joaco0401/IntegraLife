-- ============================================================
-- Integra Life — Migracion a multiusuario
-- ============================================================

-- 1. Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username        TEXT UNIQUE NOT NULL,
    nombre_visible  TEXT,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Usuarios iniciales
INSERT INTO usuarios (username, nombre_visible)
VALUES ('rodrigo', 'Rodrigo Oryan')
ON CONFLICT (username) DO NOTHING;

INSERT INTO usuarios (username, nombre_visible)
VALUES ('sofiespinoza', 'Sofia Espinoza')
ON CONFLICT (username) DO NOTHING;

-- 3. Columna usuario_id en las tablas principales
ALTER TABLE contactos      ADD COLUMN IF NOT EXISTS usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE;
ALTER TABLE empresas       ADD COLUMN IF NOT EXISTS usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE;
ALTER TABLE eventos        ADD COLUMN IF NOT EXISTS usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE;
ALTER TABLE interacciones  ADD COLUMN IF NOT EXISTS usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE;

-- 4. Todos los datos existentes pasan a ser de Rodrigo
UPDATE contactos     SET usuario_id = (SELECT id FROM usuarios WHERE username = 'rodrigo') WHERE usuario_id IS NULL;
UPDATE empresas      SET usuario_id = (SELECT id FROM usuarios WHERE username = 'rodrigo') WHERE usuario_id IS NULL;
UPDATE eventos       SET usuario_id = (SELECT id FROM usuarios WHERE username = 'rodrigo') WHERE usuario_id IS NULL;
UPDATE interacciones SET usuario_id = (SELECT id FROM usuarios WHERE username = 'rodrigo') WHERE usuario_id IS NULL;

-- 5. Indices para que las consultas filtradas sean rapidas
CREATE INDEX IF NOT EXISTS idx_contactos_usuario     ON contactos (usuario_id);
CREATE INDEX IF NOT EXISTS idx_empresas_usuario      ON empresas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_eventos_usuario       ON eventos (usuario_id);
CREATE INDEX IF NOT EXISTS idx_interacciones_usuario ON interacciones (usuario_id);

-- 6. El evento de Google ya no es unico globalmente, sino por usuario
ALTER TABLE eventos DROP CONSTRAINT IF EXISTS eventos_gcal_event_id_key;
CREATE UNIQUE INDEX IF NOT EXISTS idx_eventos_gcal_usuario ON eventos (gcal_event_id, usuario_id);

-- 7. Un mismo email puede existir para contactos de usuarios distintos
ALTER TABLE contacto_emails DROP CONSTRAINT IF EXISTS contacto_emails_email_key;
CREATE UNIQUE INDEX IF NOT EXISTS idx_contacto_emails_unico ON contacto_emails (contacto_id, lower(email));