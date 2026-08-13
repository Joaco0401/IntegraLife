-- ============================================================
-- Integra Life — Notas de voz y anotaciones de empresa
-- ============================================================

-- Notas de voz: audio original + transcripcion + analisis
CREATE TABLE IF NOT EXISTS notas_voz (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id      UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    organizacion_id UUID REFERENCES usuario_organizaciones(id) ON DELETE SET NULL,
    audio_path      TEXT,
    duracion_seg    INTEGER,
    transcripcion   TEXT,
    analisis        JSONB,
    estado          TEXT NOT NULL DEFAULT 'pendiente'
                    CHECK (estado IN ('pendiente','transcrita','analizada','aplicada','error')),
    creada_en       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notas_voz_usuario ON notas_voz (usuario_id, creada_en DESC);

-- Las interacciones ahora pueden colgar de una empresa (no solo de un contacto)
ALTER TABLE interacciones ALTER COLUMN contacto_id DROP NOT NULL;
ALTER TABLE interacciones ADD COLUMN IF NOT EXISTS empresa_id UUID
    REFERENCES empresas(id) ON DELETE CASCADE;
ALTER TABLE interacciones ADD COLUMN IF NOT EXISTS nota_voz_id UUID
    REFERENCES notas_voz(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_interacciones_empresa ON interacciones (empresa_id, fecha DESC);

-- Una interaccion debe pertenecer a un contacto o a una empresa
ALTER TABLE interacciones DROP CONSTRAINT IF EXISTS chk_interaccion_destino;
ALTER TABLE interacciones ADD CONSTRAINT chk_interaccion_destino
    CHECK (contacto_id IS NOT NULL OR empresa_id IS NOT NULL);