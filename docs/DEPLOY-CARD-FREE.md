# Card-free live deployment — HireReady Agent (Code for a Billion)

**UPDATE Oct 29, 2026: Render deployment SUCCEEDED the same day (live https://hireready-agent.onrender.com) after the user confirmed the $1 temporary authorization. This card-free pack is now a fallback guide only, NOT the live deployment. The "Render BLOCKED / do not retry" lines below are historical to the Oct 28-29 morning state and are superseded by the live Render URL in README.md and docs/SUBMISSION-DRAFT.md.**

**Status on 2026-10-29 (original): PREPARED, NOT DEPLOYED, NOT PUSHED.**
The files in this pack were written locally on 2026-10-29. They are NOT
yet in the public GitHub repo. Step 0 below (push) must happen first,
or the deploy host will clone the OLD tree without `wsgi.py`.

**Hard rules (unchanged):**
- NO card, NO payment, NO Render retry. Render is BLOCKED after two
  insufficient-funds card rejections — do not retry it.
- If ANY host asks for a card at ANY step, STOP that route immediately,
  enter nothing, and report the exact prompt. Do not upgrade, do not
  "verify with a $1 hold".
- No live URL may be claimed until it has been opened and tested
  end-to-end (Section 4). The submission draft still says TODO for the
  live URL until that test passes.

## 1. Chosen route: PythonAnywhere Beginner (primary)

Why this one, not a Docker host: HireReady is Python stdlib only, needs
no pip install, no Docker, no database, and makes NO outbound API calls
(resource links are opened by the visitor's browser, not by the server).
PythonAnywhere runs exactly that as a WSGI app, on a free Beginner
account, with a persistent home directory — so `data/store.json`
dashboard counters survive reloads, unlike serverless hosts.

What the 2026-10-29 research found (verify on the dashboard at signup;
do not treat these as a guarantee):
- Beginner account: 1 free web app at `<username>.pythonanywhere.com`,
  512 MB disk, a daily CPU-seconds limit. No card is listed for the
  Beginner tier in the sources checked.
- Free web apps must be renewed/extended from the dashboard before
  their "Run until" date — check that date on the Web tab after deploy
  and extend it (free click, no payment) before it lapses. If extending
  ever asks for payment, STOP and report it; do not pay.
- Outbound internet on free accounts is allowlisted, but this app
  needs none (see above).

### Step 0 — push this pack to GitHub first (browser/GitHub login)
Push to https://github.com/umarshareef0165-netizen/hireready-agent,
branch `main`, and verify the tree shows ALL of these new files:
`wsgi.py`, `api/index.py`, `vercel.json`, `Dockerfile.hf`,
`.dockerignore`, `docs/DEPLOY-CARD-FREE.md`,
`docs/AGENTFOUNDRY-CHECKLIST.md`, `docs/hf-space-readme.md`.
Do not deploy from a tree that lacks `wsgi.py`.

### Step 1 — create the PythonAnywhere account (no card)
1. Open pythonanywhere.com, create a Beginner (free) account.
   **STOP if a card is requested at any point.**
2. Record the exact PythonAnywhere username — the live URL will be
   `https://<username>.pythonanywhere.com`. Do not guess it in advance.

### Step 2 — clone the repo in a Bash console
```bash
git clone https://github.com/umarshareef0165-netizen/hireready-agent
cd hireready-agent
python3 -m unittest discover -s tests   # expect 9/9 OK before deploying
```

### Step 3 — create the web app (Web tab)
1. Web tab → **Add a new web app** → **Manual configuration** →
   Python 3.12 (or the newest 3.12+ offered).
   Do NOT pick a Flask/Django template — if one is picked by mistake,
   its WSGI boilerplate must still be replaced in full in Step 4.
2. Source code: `/home/<username>/hireready-agent`
   Working directory: `/home/<username>/hireready-agent`
3. Virtualenv: none needed (stdlib only). Leave blank / system default.
   No `requirements.txt` exists and none is needed. Do NOT pip-install
   anything.
4. Open the WSGI file link (named like
   `/var/www/<username>_pythonanywhere_com_wsgi.py`) and REPLACE its
   entire contents with exactly:
```python
import sys
sys.path.insert(0, '/home/<username>/hireready-agent')
from wsgi import application
```
   (Replace `<username>` with the real username. This file lives on
   PythonAnywhere only — it is intentionally NOT in this repo.)
5. Click **Reload**, then open `https://<username>.pythonanywhere.com`.

### Step 4 — live test (must all pass before the URL is claimed)
1. Home page loads, all 4 sections visible, "mock" label visible.
2. Gap flow: JD "Python developer: Python, FastAPI, SQL, Docker",
   CV mentioning FitTrack in Python with SQL, project
   "FitTrack | https://github.com/... | Python fitness tracker with SQL"
   → Python + SQL evidenced, FastAPI + Docker missing, dated plan shown.
3. Portfolio flow with the same project → portfolio + hiring signal.
4. Interview flow: role python → questions load with visible rubric →
   an answer scores and shows feedback.
5. Dashboard: counters increase by exactly the actions just done
   (gap_reports, portfolios, interviews, tasks_completed). Refresh —
   counters must NOT reset.
6. If any step fails: check the **Error log** on the Web tab, fix,
   Reload, re-test. Do not put the URL in the submission draft until
   all 5 pass.

### After a passing test
- Paste the real URL into `docs/SUBMISSION-DRAFT.md` (replacing the
  TODO) and into the GitHub submission form — only with Umar Shareef's
  final approval, before 15 Nov 2026, never in the final hour.
- Note the Web tab "Run until" date and extend it free before expiry.
- After any `git pull` on PythonAnywhere, click Reload and re-run
  Section 4, steps 2–5. `data/store.json` is gitignored and untracked,
  so a pull must not delete it; if counters ever reset, report it
  honestly instead of re-seeding them.

## 2. Fallback: Vercel Hobby (only if PythonAnywhere asks for a card)

- Import https://github.com/umarshareef0165-netizen/hireready-agent
  in Vercel, Hobby (free) plan, no environment variables, Deploy.
  **STOP if a card is requested.**
- Routing is in `vercel.json` (every path → `api/index.py`); the app
  code is the same `src/agent.py`.
- **Honest limitation:** Vercel Functions are serverless with no
  persistent filesystem, so `api/index.py` counters are in-memory only
  and reset on cold start. Gap / plan / portfolio / interview work;
  dashboard numbers on Vercel are NOT cumulative impact evidence and
  must NOT be quoted in the submission. Prefer PythonAnywhere whenever
  it works, because its counters are real.
- Vercel deployment itself has NOT been tested by the preparer
  (subagents cannot use the live browser) — the browser deployer must
  run Section 4, steps 1–4 on the Vercel URL before claiming it live,
  and must report step 5 as "not persistent on Vercel" rather than
  faking a pass.

## 3. Gated attempt only: Hugging Face Spaces (Docker) — do NOT pay

New free Hugging Face accounts were reported in Sep 2026 forum posts
as being refused Docker/Gradio Spaces on CPU Basic with a message
along the lines of "requires a PRO subscription". That is NOT settled
official policy, so this route is an attempt, never a plan:
1. Try: New Space → SDK **Docker** → Public → hardware **CPU Basic
   (FREE)**. **If creation shows PRO, a card prompt, or any payment
   step, STOP immediately — do not upgrade, do not enter a card —
   and use PythonAnywhere (Section 1) instead.**
2. Only if the Space is created free: in the Space's own repo, copy
   `src/`, `public/`, and `Dockerfile.hf` renamed to `Dockerfile`,
   plus the frontmatter in `docs/hf-space-readme.md` as the Space
   README. HF needs port 7860 and user UID 1000 — both are already in
   `Dockerfile.hf`; `src/server.py` already binds 0.0.0.0 on `$PORT`.
3. Wait for build green, then run Section 4, steps 1–5 on the
   `https://<owner>-<space>.hf.space` URL. Dashboard counters on HF
   are in the container's writable layer, not guaranteed persistent —
   if they reset, report that honestly; do not seed them.

## 4. Hosts deliberately NOT used (2026-10-29 research)

| Host | Why not |
|---|---|
| Render | BLOCKED for this project: card demanded even for free, rejected twice for insufficient funds. Do not retry. |
| Koyeb | Since Feb 2026, new accounts are reported to require a card with a $29 pre-authorisation hold. Excluded. |
| Fly.io | No free tier for new accounts; card required after a short trial. Excluded. |
| Google Cloud Run / AWS Lambda / Azure | Billing account / card required even inside free allowances. Excluded. |
| Railway | One-time $5 trial credit, then a $1/month free credit that does not cover an always-on service; Hobby needs a card. Not a reliable live-demo host. Excluded. |

## 5. What this pack does NOT change

- Local run is unchanged: `python3 src/server.py` → http://localhost:8002/
- Tests are unchanged: `python3 -m unittest discover -s tests` (9/9).
- Licence Apache-2.0, impact area Tech Employment for Youth, solo
  builder Umar Shareef, no NGO partner, no pilot users, no invented
  stats — see `docs/AGENTFOUNDRY-CHECKLIST.md` for the remaining chain.
