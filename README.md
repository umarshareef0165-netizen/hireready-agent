# HireReady Agent — Code for a Billion 2026

**Impact area:** Tech Employment for Youth (Umar Shareef's registered area).
**Problem (as registered, no invented statistics):** Young people in Pakistan,
including final-year computer science students in Faisalabad, lack practical,
job-ready AI skills, mentorship, and a clear pathway to paid tech employment,
so strong academic learning does not convert into real tech jobs.

## What it does — one sentence
An agentic AI coach that turns a student's CV + GitHub links + a pasted job
description into a skill-gap report, a dated learning plan, a verified
portfolio page, and a mock-interview practice loop — with every claim tied to
evidence the student actually produced.

## Agentic pipeline (not a single prompt)
Planner → SkillExtractor → GapAnalyser → PlanBuilder → PortfolioBuilder →
Interviewer/Feedback → Dashboard counters. See `src/agent.py`.

## The evidence rule — the whole point
- **evidenced** — skill is in the CV text AND linked to a real project/task supplied.
- **claimed, not evidenced** — skill is in the CV but no linked project/task supplied.
- **missing** — skill required by the job description but absent from the CV.
- Nothing is ever invented: no fake jobs, employers, certificates, placements,
  or job guarantees. No job scraping, no employer matching.

## Features (nothing skipped)
1. Skill-gap report (ranked gaps, one learning task per gap)
2. Dated, bite-size learning plan with free official resources
3. Verified portfolio page + hiring-signal summary (supplied projects only)
4. Mock interview for Python / ML / full-stack / agentic AI, scored against a
   **visible rubric** (keywords shown before answering, specific feedback after)
5. Honest impact dashboard — counters count only real in-app actions in this
   deployment (`data/store.json`, gitignored, never seeded as real users)

## Run locally (mock mode, no key needed)
```bash
cd hireready-agent
python3 src/server.py        # http://localhost:8002/
python3 -m unittest discover -s tests
```
Try: JD "Python developer: Python, FastAPI, SQL, Docker", CV mentioning
FitTrack in Python with SQL, project "FitTrack | https://github.com/... |
Python fitness tracker with SQL" → Python + SQL evidenced, FastAPI + Docker missing.

## Deploy — LIVE on Render
Live demo: https://hireready-agent.onrender.com
- Service hireready-agent, Docker, Free plan, region Oregon (US West), branch main, commit 3757a20, "Deploy succeeded" / "Live" on Oct 29, 2026, 5-point live test passed the same day (home, FitTrack gap, portfolio, interview 9/10, dashboard surviving reload).
- Python stdlib only, no pip install. Local run: `python3 src/server.py` (http://localhost:8002/).
- Card-free alternatives prepared in `docs/DEPLOY-CARD-FREE.md` (PythonAnywhere Beginner WSGI via `wsgi.py`, Vercel Hobby via `api/index.py`, gated Hugging Face Spaces Docker via `Dockerfile.hf`) were NOT used as the live deployment; the PythonAnywhere fallback was stopped after Render succeeded.
- Live dashboard counters 1 / 1 / 1 / 0 at deploy time are builder test actions from the verified live test, NOT pilot users and NOT real students.

## Out of scope (deliberately)
Job scraping, employer matching, paid placements, certificates, job guarantees,
AgentFoundry usage claims (see below), NGO partners.

## Honest status
- **Mock mode:** skill extraction is deterministic keyword matching. A real-LLM
  adapter stub is in `src/real_llm.py` and is NOT wired in. Do not claim live AI
  until it is implemented, live-tested, and the README is updated.
- **AgentFoundry:** JUDGING.md lists "Built using AgentFoundry (AF), the official IDE" under Eligibility, so a real AgentFoundry project step is in progress and is NOT claimed yet. Do not claim "built in AgentFoundry" on the basis of this local repo alone.
- **NGO partner:** none invented, none claimed. The welcome email says to sign up with a local NGO/partner of choice, but the official page / JUDGING.md fetched Oct 29, 2026 contain no mandatory partner field or evidence requirement — see `~/workspace/code-for-a-billion/TC-RESEARCH-2026-10-29.md` and candidate-only list in `docs/NGO-CANDIDATES.md` (not in this repo).
- **Proven impact:** in an 18-day window this will be thin. Report only real
  counts from the dashboard, never inflated numbers.
- **No win is guaranteed.**

## Licence
Apache-2.0 (see `LICENSE`) — per Code for India open-source rules.

## Submission checklist
See `docs/SUBMISSION-CHECKLIST.md`. Submit only with Umar Shareef's approval,
well before 15 Nov 2026, never in the final hour. Winners: 5 Dec 2026.
