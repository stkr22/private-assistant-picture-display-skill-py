-- Migration: Add min_vibrancy_score to immich_sync_jobs
-- Date: 2026-04-11

ALTER TABLE immich_sync_jobs
    ADD COLUMN IF NOT EXISTS min_vibrancy_score FLOAT DEFAULT 0.2;

COMMENT ON COLUMN immich_sync_jobs.min_vibrancy_score IS
    'Minimum vibrancy score (0.0-1.0) for e-ink display suitability. 0.0 = disabled.';
