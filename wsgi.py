"""HireReady Agent — WSGI entry point for PythonAnywhere (Beginner, no card).

This is the SAME app as src/server.py, with the same routes, the same
agent pipeline (src/agent.py, Python stdlib only) and the same honest
dashboard counters in data/store.json (gitignored, never seeded).
It exists because PythonAnywhere runs WSGI apps, not the stdlib
http.server used locally, and because Render is BLOCKED for this
project (card rejected twice — do not retry Render, do not enter a card).

PythonAnywhere WSGI file (created in the dashboard, NOT in this repo)
should contain only:
    import sys
    sys.path.insert(0, '/home/<username>/hireready-agent')
    from wsgi import application

Replace <username> with the real PythonAnywhere username at deploy time.
No secrets, no API keys, no environment variables are required.
"""
import json
import os
import sys
import threading

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "src"))

from agent import gap_report, learning_plan, portfolio, interview_questions, score_answer  # noqa: E402

DATA_DIR = os.path.join(BASE, "data")
STORE = os.path.join(DATA_DIR, "store.json")
_LOCK = threading.Lock()


def _load_store():
    try:
        with open(STORE) as f:
            return json.load(f)
    except Exception:
        return {"gap_reports": 0, "portfolios": 0, "interviews": 0, "tasks_completed": 0, "plans": []}


def _save_store(store):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STORE, "w") as f:
        json.dump(store, f, indent=2)


def _static_index():
    with open(os.path.join(BASE, "public", "index.html"), "rb") as f:
        return f.read()


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/") or "/"
    body = {}
    if method == "POST":
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            length = 0
        raw = environ["wsgi.input"].read(length) if length > 0 else b"{}"
        try:
            body = json.loads(raw or b"{}")
        except Exception:
            body = {}

    def respond(status, payload, content_type="application/json"):
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        start_response(status, [("Content-Type", content_type), ("Content-Length", str(len(data)))])
        return [data]

    if method == "GET" and path in ("/", "/index.html"):
        return respond("200 OK", _static_index(), "text/html")
    if method == "GET" and path == "/api/dashboard":
        return respond("200 OK", _load_store())
    if method == "POST":
        with _LOCK:
            store = _load_store()
            if path == "/api/gap":
                if not body.get("job_description") or not body.get("cv_text"):
                    return respond("400 Bad Request", {"error": "job_description and cv_text are required"})
                gap = gap_report(body["job_description"], body["cv_text"], body.get("projects", []))
                plan = learning_plan(gap)
                store["gap_reports"] += 1
                store["plans"].append(plan)
                _save_store(store)
                return respond("200 OK", {"gap": gap, "plan": plan, "mode": "mock — deterministic skill extraction, no LLM key used"})
            if path == "/api/portfolio":
                if not body.get("projects"):
                    return respond("400 Bad Request", {"error": "at least one real project is required"})
                gap = gap_report(body.get("job_description", ""), body.get("cv_text", ""), body["projects"])
                store["portfolios"] += 1
                _save_store(store)
                return respond("200 OK", portfolio(body["projects"], gap))
            if path == "/api/interview/questions":
                return respond("200 OK", {"questions": interview_questions(body.get("role", "python"))})
            if path == "/api/interview/score":
                questions = interview_questions(body.get("role", "python"))
                try:
                    question = questions[int(body.get("index", 0))]
                except Exception:
                    return respond("400 Bad Request", {"error": "invalid question index"})
                store["interviews"] += 1
                _save_store(store)
                return respond("200 OK", score_answer(question, body.get("answer", "")))
            if path == "/api/task/done":
                store["tasks_completed"] += 1
                _save_store(store)
                return respond("200 OK", {"ok": True, "tasks_completed": store["tasks_completed"]})
    return respond("404 Not Found", {"error": "not found"})
