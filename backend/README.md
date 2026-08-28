# Building Code Assistant — backend

A minimal API-key-based backend for the Building Code tab: staff type a
question into `static/index.html` (embedded in the Google Site), it hits
this backend, which answers using Claude with the office's building code
documents as context. No per-seat Claude license needed — just one API
key and usage-based billing.

This covers **building code questions only**. Office standards/templates/
contracts (the locked Google Drive folder) are a separate integration —
not built here yet.

## How it decides which model to use

Every question first goes to **Claude Sonnet 5** (cheaper, $2/$10 per
million input/output tokens). Sonnet answers directly for the vast
majority of questions — most building-code lookups are "what does section
X say," not deep reasoning. Sonnet is instructed to flag a question as
needing escalation only when it genuinely requires cross-referencing
multiple sections or resolving a conflict between them; only those get
re-asked with **Claude Opus 5** ($5/$25 per million). This should stay a
small minority of traffic — most costs come from Sonnet.

## Why cost stays manageable at 30 people

The building code text is loaded once per request but marked as a single
cached block (`cache_control` with a 1-hour TTL). Every staff member's
question shares the exact same cached prefix, so the whole office rides
on the same cache entry — the first question in a given hour pays the
"cache write" price, everyone after that in the same hour pays the much
cheaper "cache read" price (roughly 1/20th of the write cost, per
million tokens).

**Illustrative example (not a quote — depends on how much code text you
load and how often people ask):**

Assume ~30,000 tokens of loaded building code text, and questions spread
across an 8-hour workday such that each hour sees at least one question
(triggering one cache write) and the rest of that hour's questions hit
cache:

- Cache write (1 per hour, 8/day): ~$0.12 each → ~$0.96/day
- Cache read (rest of the questions, say 40/day): ~$0.006 each → ~$0.25/day
- Small per-question cost (the question itself + the answer): a few cents/day total

That's roughly **$1–2/day, or $25–40/month**, for the whole office — and
this scales with how much code text you load (a single jurisdiction's
relevant chapters, not an entire multi-state code library) and how often
people actually ask. Occasional Opus escalations add a bit more (Opus's
cache write/read costs more per token), but should stay rare if the
escalation rule holds.

**Watch actual spend** in the Anthropic Console's usage dashboard once
this is live, rather than trusting this estimate — real question volume
and document size will move these numbers. If it runs higher than
expected, the first lever is trimming the loaded documents to just the
sections staff actually ask about, not code changes.

## Setup

1. **Add the real building code documents.** This backend reads plain
   text/Markdown files from `../knowledge/building-code/`. If your source
   documents are PDFs, convert them to text first (e.g. `pdftotext`) and
   drop the `.txt` files there. There's nothing to answer from until real
   documents replace the placeholder README in that folder.

2. **Install dependencies locally to test:**
   ```bash
   cd backend
   pip install -r requirements.txt
   export ANTHROPIC_API_KEY=sk-ant-...
   functions-framework --target=building_code_qa --debug
   ```
   Then `curl -X POST localhost:8080 -H "Content-Type: application/json" -d '{"question": "..."}'`.

3. **Deploy to Google Cloud Functions (2nd gen)** — fits naturally next
   to a Google Workspace / Google Sites setup:
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
   - Store the API key in **Secret Manager** (`anthropic-api-key`), not as
     a plain `--set-env-vars` value — it's the same key for the whole
     office, worth protecting.
   - Set `ALLOWED_ORIGIN` to your actual published Google Site's origin
     (the exact `https://...` the browser sends, which may differ from
     `sites.google.com` if you're on a custom domain) so only your site's
     page can call this function from a browser. This is a basic guard,
     not strong auth — see "Hardening" below before treating this as done.
   - `--allow-unauthenticated` is required so the browser-side widget can
     call it directly with no login step, matching the "click and ask"
     experience non-technical staff need.

4. **Host `static/index.html` somewhere with a public URL** (Firebase
   Hosting, GitHub Pages, or a Cloud Storage static bucket all work) after
   replacing `REPLACE_WITH_YOUR_DEPLOYED_FUNCTION_URL` with the Cloud
   Function's URL from step 3.

5. **Embed it in Google Sites:** on the Building Code tab, use
   **Insert → Embed → By URL** and paste the hosted page's URL. Google
   Sites can't run this chat widget natively — it embeds it as an iframe.

## Hardening before wider rollout

This is a working reference, not a finished production setup. Before
opening it to the whole office, consider:

- The CORS `ALLOWED_ORIGIN` check only stops *browser* requests from other
  origins — it doesn't stop someone who has the function's URL from
  calling it directly with `curl`. If that matters, add a lightweight
  shared secret the widget sends and the function checks, or put the
  function behind Cloud Run with Identity-Aware Proxy / Google
  Workspace-restricted access.
- No rate limiting yet. One person accidentally hammering the endpoint
  could run up cost. Cloud Functions/Run has built-in concurrency limits,
  but consider a simple per-IP or per-day cap if this becomes a concern.
- No logging/monitoring dashboard beyond Cloud Functions' own logs
  (`model_used`, cache stats are logged per request — see `app.py`).
