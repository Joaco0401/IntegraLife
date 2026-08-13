ALTER TABLE empresas ADD COLUMN IF NOT EXISTS organizacion_id UUID
    REFERENCES usuario_organizaciones(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_empresas_org ON empresas (usuario_id, organizacion_id);