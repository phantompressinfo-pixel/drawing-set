# Building Code Assistant — backend

An API-key-based backend for the Building Code tab: staff type a question
into `static/index.html` (embedded in the Google Site), it hits this
backend, which searches `code-library/` and answers with Claude. No
per-seat Claude license needed — just one API key and usage-based
billing.

This covers **building code questions only**. Office standards/templates/
contracts (the locked Google Drive folder) are a separate integration —
not built here.

## How it answers

`code-library/` is large (the full Aspen and Pitkin County code text,
plus the model IBC/IRC/IEBC/ADA text as adopted by Colorado and GSA) — far
too large to hand to Claude as one block of context. Instead, Claude gets
two search tools (`code_search.py`) and runs its own search loop, the same
way `.claude/skills/us-building-codes` and `.claude/skills/aspen-pitkin-code`
already work in Claude Code:

- `search_model_codes` — the model code CSVs (IBC/IRC/IEBC, ADA), with the
  same amendment/DPO flagging `codesearch.py` already does. If a hit is
  flagged as locally amended or Colorado-diverged, the model is instructed
  to say so rather than presenting superseded text as the requirement.
- `search_local_code` — greps the Aspen/Pitkin code text directly.
- `escalate_to_expert_review` — Claude calls this itself instead of
  answering when a question needs real cross-referencing or judgment,
  rather than a direct lookup. When it does, the whole question is re-run
  from scratch on Opus 5.

**Every question first goes to Claude Sonnet 5** ($2/$10 per million
input/output tokens). Only questions Sonnet itself flags as needing
deeper reasoning get re-asked with **Claude Opus 5** ($5/$25 per
million) — that should stay a small minority of traffic.

See `code_search.py` and the two `.claude/skills/` folders it wraps for
the actual search/amendment logic — it's not duplicated here, so the
backend and Claude Code stay in sync instead of drifting apart.

## Why this is cheap per question

Each question triggers a handful of small tool calls (a search returns a
capped number of matching sections, not the whole library) plus a short
final answer — not thousands of tokens of static document dumped into
every request. The one static, repeated part — the system instructions —
is marked `cache_control` so it's cheap to re-send across questions, but
the bulk of the cost here is naturally small because retrieval is
targeted. Expect this to run cheaper than a "cache the whole document"
design would have, and cheaper by a wide margin than 30 per-seat Claude
licenses.

**Watch actual spend** in the Anthropic Console's usage dashboard once
this is live — a real number beats an estimate here, since it depends on
how deep Claude's search loop goes per question and how often questions
escalate to Opus.

## Setup

1. **Install dependencies locally to test:**
   ```bash
   cd backend
   pip install -r requirements.txt
   export ANTHROPIC_API_KEY=sk-ant-...
   functions-framework --target=building_code_qa --debug
   ```
   Then `curl -X POST localhost:8080 -H "Content-Type: application/json" -d '{"question": "..."}'`.

   Note: this uses the Anthropic Python SDK's **Tool Runner** (`client.beta.messages.tool_runner`),
   which is a beta feature — make sure your installed `anthropic` package
   version supports it (a recent 1.x release).

2. **Deploy to Google Cloud Functions (2nd gen)** — fits naturally next
   to a Google Workspace / Google Sites setup. Deploy from the **repo
   root**, not `backend/`, since `app.py` reads `code-library/` and
   `.claude/skills/us-building-codes/scripts/codesearch.py` via paths
   relative to the repo root:
   ```bash
   gcloud functions deploy building-code-qa \
     --gen2 \
     --runtime=python312 \
     --region=us-central1 \
     --source=. \
     --entry-point=building_code_qa \
     --trigger-http \
     --allow-unauthenticated \
     --set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest \
     --set-env-vars=ALLOWED_ORIGIN=https://sites.google.com
   ```
   You'll need a small tweak either way: Cloud Functions packages only
   the `--source` directory, so either point `--source` at the repo root
   and add an `entry_point` shim that imports `backend/app.py`, or copy/
   symlink `code-library/` and `.claude/skills/us-building-codes/scripts/`
   into `backend/` at deploy time. Pick whichever fits your deploy
   pipeline — the important part is that both paths are present relative
   to wherever `app.py` actually runs.
   - Store the API key in **Secret Manager** (`anthropic-api-key`), not as
     a plain `--set-env-vars` value.
   - Set `ALLOWED_ORIGIN` to your actual published Google Site's origin
     (the exact `https://...` the browser sends, which may differ from
     `sites.google.com` if you're on a custom domain).
   - `--allow-unauthenticated` is required so the browser-side widget can
     call it directly with no login step.

3. **Host `static/index.html` somewhere with a public URL** (Firebase
   Hosting, GitHub Pages, or a Cloud Storage static bucket all work) after
   replacing `REPLACE_WITH_YOUR_DEPLOYED_FUNCTION_URL` with the Cloud
   Function's URL from step 2.

4. **Embed it in Google Sites:** on the Building Code tab, use
   **Insert → Embed → By URL** and paste the hosted page's URL.

## Hardening before wider rollout

This is a working reference, not a finished production setup:

- The CORS `ALLOWED_ORIGIN` check only stops *browser* requests from other
  origins — it doesn't stop someone with the function's URL from calling
  it directly. If that matters, add a shared secret the widget sends and
  the function checks, or put it behind Cloud Run with Identity-Aware
  Proxy / Google Workspace-restricted access.
- No rate limiting yet. Consider a per-IP or per-day cap if cost becomes
  a concern — each question can trigger several tool calls before Sonnet
  answers, and an Opus escalation costs more still.
- No dedicated logging/monitoring dashboard beyond Cloud Functions' own
  logs (`model_used` and the tool-call count are logged per request — see
  `app.py`).
- This has not been run against the live Claude API in this environment
  (no credentials here) — test it end-to-end with a real API key before
  trusting it in front of the whole office.
