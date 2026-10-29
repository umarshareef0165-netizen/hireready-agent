"""HireReady Agent — Vercel fallback ONLY (not the primary route).

Primary route is PythonAnywhere (see docs/DEPLOY-CARD-FREE.md).
This file exists so a Vercel Hobby deploy (no card, per Vercel's own
free-tier terms) can be attempted in one step IF PythonAnywhere asks
for a card at signup — in that case STOP the PythonAnywhere route and
use this one, and report the card prompt.

LIMITATION, stated honestly: Vercel Functions are serverless and the
filesystem is not persistent, so the dashboard counters here are
in-memory only and reset on cold start. They are NOT cumulative impact
evidence. Do NOT quote Vercel dashboard numbers in the submission.
Gap reports, learning plans, portfolios and mock interviews all work
exactly as in the local app (same src/agent.py, stdlib only).

Routing: vercel.json rewrites every path to this file; handle_request()
is the pure, locally testable core, and `handler` is the Vercel
BaseHTTPRequestHandler wrapper around it.
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "src"))

from agent import gap_report, learning_plan, portfolio, interview_questions, score_answer  # noqa: E402

_COUNTERS = {"gap_reports": 0, "portfolios": 0, "interviews": 0, "tasks_completed": 0}


def handle_request(method, path, body):
    """Pure core: returns (status_code:int, payload:dict|bytes, content_type:str)."""
    body = body or {}
    if method == "GET" and path in ("/", "/index.html"):
        with open(os.path.join(BASE, "public", "index.html"), "rb") as f:
            return 200, f.read(), "text/html"
    if method == "GET" and path == "/api/dashboard":
        return 200, dict(_COUNTERS, note="serverless instance counters only — reset on cold start, NOT cumulative impact"), "application/json"
    if method == "POST" and path == "/api/gap":
        if not body.get("job_description") or not body.get("cv_text"):
            return 400, {"error": "job_description and cv_text are required"}, "application/json"
        gap = gap_report(body["job_description"], body["cv_text"], body.get("projects", []))
        _COUNTERS["gap_reports"] += 1
        return 200, {"gap": gap, "plan": learning_plan(gap), "mode": "mock — deterministic skill extraction, no LLM key used"}, "application/json"
    if method == "POST" and path == "/api/portfolio":
        if not body.get("projects"):
            return 400, {"error": "at least one real project is required"}, "application/json"
        gap = gap_report(body.get("job_description", ""), body.get("cv_text", ""), body["projects"])
        _COUNTERS["portfolios"] += 1
        return 200, portfolio(body["projects"], gap), "application/json"
    if method == "POST" and path == "/api/interview/questions":
        return 200, {"questions": interview_questions(body.get("role", "python"))}, "application/json"
    if method == "POST" and path == "/api/interview/score":
        questions = interview_questions(body.get("role", "python"))
        try:
            question = questions[int(body.get("index", 0))]
        except Exception:
            return 400, {"error": "invalid question index"}, "application/json"
        _COUNTERS["interviews"] += 1
        return 200, score_answer(question, body.get("answer", "")), "application/json"
    if method == "POST" and path == "/api/task/done":
        _COUNTERS["tasks_completed"] += 1
        return 200, {"ok": True, "tasks_completed": _COUNTERS["tasks_completed"]}, "application/json"
    return 404, {"error": "not found"}, "application/json"


try:
    from http.server import BaseHTTPRequestHandler

    class handler(BaseHTTPRequestHandler):
        def _handle(self, method):
            length = int(self.headers.get("Content-Length", 0) or 0)
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                body = json.loads(raw or b"{}")
            except Exception:
                body = {}
            status, payload, content_type = handle_request(method, self.path.split("?")[0], body)
            data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self._handle("GET")

        def do_POST(self):
            self._handle("POST")

        def log_message(self, *args):  # keep Vercel logs clean
            pass

except ImportError:  # pragma: no cover
    pass
