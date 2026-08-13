-- ============================================================
-- Integra Life — Vista organizacion vs personal
-- ============================================================

-- Cada usuario puede declarar cual es su propia empresa
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS empresa_propia_id UUID REFERENCES empresas(id) ON DELETE SET NULL;

-- Indice para las consultas filtradas por empresa
CREATE INDEX IF NOT EXISTS idx_contactos_empresa_usuario ON contactos (usuario_id, empresa_id);