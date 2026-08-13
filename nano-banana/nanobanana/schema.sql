-- Nano Banana prompt database.
-- Holds the 7-section template definition, the vocabulary that drives it,
-- and every prompt/render produced from it.

PRAGMA foreign_keys = ON;

-- json_path is where the section actually lands in the output. Six sections are
-- top-level keys; physics_accuracy is documented by the skill as a field inside
-- technical_specifications, which is why the template says "7 sections" but the
-- JSON block shows six keys.
CREATE TABLE IF NOT EXISTS sections (
    id          INTEGER PRIMARY KEY,
    key         TEXT NOT NULL UNIQUE,
    ordinal     INTEGER NOT NULL,
    json_path   TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fields (
    id         INTEGER PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    key        TEXT NOT NULL,
    guidance   TEXT NOT NULL,
    examples   TEXT NOT NULL DEFAULT '',
    UNIQUE (section_id, key)
);

-- kind: 'lighting' | 'mood' | 'reference'
-- trigger: the scene cue that selects this value ('golden hour', 'hotel corridor', ...)
CREATE TABLE IF NOT EXISTS vocabulary (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,
    trigger TEXT NOT NULL,
    value   TEXT NOT NULL,
    UNIQUE (kind, trigger)
);

-- bucket: 'include' | 'avoid'
CREATE TABLE IF NOT EXISTS quality_keywords (
    id     INTEGER PRIMARY KEY,
    bucket TEXT NOT NULL,
    term   TEXT NOT NULL,
    UNIQUE (bucket, term)
);

CREATE TABLE IF NOT EXISTS prompts (
    id          INTEGER PRIMARY KEY,
    created_at  TEXT NOT NULL,
    source_path TEXT,
    image_sha256 TEXT,
    model       TEXT NOT NULL,
    scene_type  TEXT,
    mood        TEXT,
    note        TEXT,
    body        TEXT NOT NULL,          -- the 7-section JSON, verbatim
    commentary  TEXT                    -- the model's 1-2 sentence read on the image
);

CREATE INDEX IF NOT EXISTS prompts_created_at ON prompts (created_at DESC);
CREATE INDEX IF NOT EXISTS prompts_image_sha ON prompts (image_sha256);

CREATE TABLE IF NOT EXISTS renders (
    id          INTEGER PRIMARY KEY,
    prompt_id   INTEGER NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    created_at  TEXT NOT NULL,
    model       TEXT NOT NULL,
    output_path TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS renders_prompt_id ON renders (prompt_id);
