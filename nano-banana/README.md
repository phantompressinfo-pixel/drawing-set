# Nano Banana

The `gemini-nano-banana-prompt` skill, rebuilt as a database and a CLI you can run
against the Gemini API.

The skill only worked inside Claude. This does the same job three ways:

1. **Database** — the template, its field guide, and the lighting/mood/reference
   vocabulary live in SQLite. Edit a row, and every prompt after it changes.
2. **CLI** — point it at a photo, get the 7-section JSON prompt back, validated
   and stored. Feed a stored prompt to the image model to render it.
3. **Paste-ready** — [`gem-instructions.md`](gem-instructions.md) is the whole
   template as one block of text for a Gemini Gem or AI Studio, if you'd rather
   not run anything.

## Setup

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=...        # https://aistudio.google.com/apikey
python -m nanobanana init
```

`init` creates `prompts.db` and loads the template into it. It's safe to re-run.

## Use

```bash
# photo -> JSON prompt, validated and saved
python -m nanobanana generate photo.jpg

# steer a single image without editing the template
python -m nanobanana generate photo.jpg -d "treat it as blue hour, not golden"

# what have I made
python -m nanobanana list
python -m nanobanana list -s "hotel corridor"
python -m nanobanana show 7

# stored prompt -> generated image
python -m nanobanana render 7 -o out.png

# use the original photo as a visual reference alongside the prompt
python -m nanobanana render 7 --reference photo.jpg -o out.png

# check a prompt you wrote by hand
python -m nanobanana validate my-prompt.json
cat my-prompt.json | python -m nanobanana validate -

# take it elsewhere
python -m nanobanana export -o prompts.jsonl
python -m nanobanana instruction -o gem-instructions.md
```

`generate` and `validate` exit `0` when clean, `2` when the prompt is usable but
the validator raised warnings, and `1` on a hard failure — so you can gate a
batch script on prompt quality.

## Using it in the Gemini app instead

Open [gem-instructions.md](gem-instructions.md), copy the whole file, and paste it
into a new Gem's instructions (Gemini → Gems → New Gem) or into the system
instructions box in AI Studio. Then upload a photo and ask for a prompt. That
file is generated from the database, so regenerate it after you edit the
template:

```bash
python -m nanobanana instruction -o gem-instructions.md
```

## Editing the template

Nothing about the template is hardcoded in the prompt-building path — it's read
out of the database every run. To add a mood for a scene type you shoot often:

```sql
INSERT INTO vocabulary (kind, trigger, value)
VALUES ('mood', 'desert highway', 'wide open, restless, sun-bleached');
```

Same for `sections`, `fields` and `quality_keywords`. `python -m nanobanana
instruction` will show the change immediately. To throw away your edits and go
back to the shipped template, run `python -m nanobanana init --reseed` — this
resets the template tables only and leaves your saved prompts alone.

## What the validator checks

Errors (prompt is structurally wrong, regenerate it):

- every section present and non-empty, including the nested
  `technical_specifications.physics_accuracy`
- `quality_keywords` has all three of `include`, `avoid`, `reference`
- `style_definition.lighting` present

Warnings (usable but thin):

- mood isn't 3–5 words
- fewer than 3 material surfaces actually described
- lighting doesn't state a colour temperature or a direction
- `avoid` is missing one of the four baseline terms
- filler words — "beautiful", "stunning", "nice" — anywhere in the prompt

## A note on "7 sections"

The original skill says seven sections but its JSON block has six top-level keys,
because it lists `physics_accuracy` as a field inside `technical_specifications`.
This keeps the output shape exactly as the skill's JSON block has it — six
top-level keys — and treats `physics_accuracy` as the seventh section, nested
where the skill puts it. The `sections.json_path` column records where each one
lands, so if you'd rather promote it to a top-level key, change that one value:

```sql
UPDATE sections SET json_path = 'physics_accuracy' WHERE key = 'physics_accuracy';
```

The instruction builder and the validator both follow `json_path`, so they stay
in agreement with each other.

## Models

Defaults are `gemini-2.5-flash` for reading images and `gemini-2.5-flash-image`
(Nano Banana) for generating them. Override per-run with `-m`, or set
`NANO_BANANA_TEXT_MODEL` / `NANO_BANANA_IMAGE_MODEL` to point at a newer model
without touching code.

## Layout

```
nanobanana/
  schema.sql       tables: template, vocabulary, prompts, renders
  seed_data.py     the template itself, as data
  db.py            queries and storage
  instruction.py   database -> Gemini system instruction
  validator.py     the skill's quality checklist, as code
  gemini.py        API calls
  cli.py           commands
tests/             python -m unittest discover -s tests
```

## Tests

```bash
python -m unittest discover -s tests
```

16 tests, no API key or network needed — they run against an in-memory database.
