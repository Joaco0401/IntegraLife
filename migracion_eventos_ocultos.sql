-- Eventos de Google que el usuario elimino y no deben volver a importarse
CREATE TABLE IF NOT EXISTS eventos_ocultos (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id     UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    gcal_event_id  TEXT NOT NULL,
    titulo         TEXT,
    ocultado_en    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (usuario_id, gcal_event_id)
);
CREATE INDEX IF NOT EXISTS idx_eventos_ocultos ON eventos_ocultos (usuario_id, gcal_event_id);