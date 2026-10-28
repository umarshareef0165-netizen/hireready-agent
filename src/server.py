"""HireReady Agent server — Python stdlib only. Run: python3 src/server.py
Port: $PORT or 8002. Data (real in-app counters only) lives in data/store.json,
which is gitignored — never committed, never inflated, never seeded as real users.
Mock mode is the default: no LLM key is required or read. A real LLM adapter
stub lives in src/real_llm.py and is NOT wired in until a live check passes.
"""
import json, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
sys.path.insert(0, os.path.dirname(__file__))
from agent import gap_report, learning_plan, portfolio, interview_questions, score_answer

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
STORE = os.path.join(DATA_DIR, "store.json")

def load_store():
    try:
        with open(STORE) as f:
            return json.load(f)
    except Exception:
        return {"gap_reports": 0, "portfolios": 0, "interviews": 0, "tasks_completed": 0, "plans": []}

def save_store(s):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STORE, "w") as f:
        json.dump(s, f, indent=2)

class H(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def _body(self):
        try: return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0) or b"{}")
        except Exception: return {}
    def _static(self, path, ctype):
        try:
            with open(os.path.join(BASE, "public", path), "rb") as f: data = f.read()
        except FileNotFoundError:
            return self._send({"error": "not found"}, 404)
        self.send_response(200); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        p = urlparse(self.path).path
        if p in ("/", "/index.html"): return self._static("index.html", "text/html")
        if p == "/api/dashboard": return self._send(load_store())
        return self._send({"error": "not found"}, 404)
    def do_POST(self):
        p = urlparse(self.path).path; b = self._body(); s = load_store()
        if p == "/api/gap":
            if not b.get("job_description") or not b.get("cv_text"):
                return self._send({"error": "job_description and cv_text are required"}, 400)
            gap = gap_report(b["job_description"], b["cv_text"], b.get("projects", []))
            plan = learning_plan(gap)
            s["gap_reports"] += 1; s["plans"].append(plan); save_store(s)
            return self._send({"gap": gap, "plan": plan, "mode": "mock — deterministic skill extraction, no LLM key used"})
        if p == "/api/portfolio":
            if not b.get("projects"):
                return self._send({"error": "at least one real project is required"}, 400)
            gap = gap_report(b.get("job_description", ""), b.get("cv_text", ""), b["projects"])
            s["portfolios"] += 1; save_store(s)
            return self._send(portfolio(b["projects"], gap))
        if p == "/api/interview/questions":
            return self._send({"questions": interview_questions(b.get("role", "python"))})
        if p == "/api/interview/score":
            qs = interview_questions(b.get("role", "python"))
            try: q = qs[int(b.get("index", 0))]
            except Exception: return self._send({"error": "invalid question index"}, 400)
            s["interviews"] += 1; save_store(s)
            return self._send(score_answer(q, b.get("answer", "")))
        if p == "/api/task/done":
            s["tasks_completed"] += 1; save_store(s); return self._send({"ok": True, "tasks_completed": s["tasks_completed"]})
        return self._send({"error": "not found"}, 404)
    def log_message(self, *a): pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8002"))
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
    print(f"HireReady Agent on http://localhost:{port}/")
