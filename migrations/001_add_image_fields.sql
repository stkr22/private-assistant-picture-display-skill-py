-- Migration: Add tags, created_at, updated_at fields to images table
-- Issue: #32
-- Date: 2026-01-01

-- Add new columns with defaults
ALTER TABLE images
    ADD COLUMN IF NOT EXISTS tags TEXT DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Migrate data from fetched_at to created_at (if fetched_at exists)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'images' AND column_name = 'fetched_at'
    ) THEN
        UPDATE images SET created_at = fetched_at WHERE created_at IS NULL OR created_at = NOW();
    END IF;
END $$;

-- Drop the deprecated fetched_at column
ALTER TABLE images DROP COLUMN IF EXISTS fetched_at;

-- Add comment for documentation
COMMENT ON COLUMN images.tags IS 'Comma-separated tags for categorization';
COMMENT ON COLUMN images.created_at IS 'When record was created (replaces fetched_at)';
COMMENT ON COLUMN images.updated_at IS 'When record was last updated';
