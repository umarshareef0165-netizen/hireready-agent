"""HireReady Agent — agentic pipeline, pure Python stdlib.

Pipeline (genuinely multi-step, not a single prompt):
  Planner -> SkillExtractor -> GapAnalyser -> PlanBuilder -> PortfolioBuilder
  -> Interviewer/Feedback -> Dashboard counters (real in-app actions only)

Evidence rule (hard, never relaxed):
  A skill is "evidenced" ONLY when it appears in the CV text AND is linked
  to a real project/task the student supplied (name + link or description).
  A skill in the CV with no linked project is "claimed, not evidenced".
  A skill required by the job description but absent from the CV is "missing".
  Nothing is ever invented: no fake jobs, employers, certificates or placements.
"""
import re
from datetime import date, timedelta

SKILLS = {
    "python": ["python"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "react": ["react"],
    "next.js": ["next.js", "nextjs"],
    "node.js": ["node", "node.js"],
    "fastapi": ["fastapi"],
    "sql": ["sql", "postgres", "postgresql", "mysql"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "agentic ai": ["agentic ai", "ai agents", "agent"],
    "llm": ["llm", "large language model"],
    "git": ["git", "github"],
    "docker": ["docker"],
    "html/css": ["html", "css"],
    "data analysis": ["data analysis", "pandas", "numpy"],
    "api design": ["api", "rest api"],
    "testing": ["testing", "pytest", "unit test"],
}

RESOURCES = {
    "python": "https://docs.python.org/3/tutorial/",
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "typescript": "https://www.typescriptlang.org/docs/",
    "react": "https://react.dev/learn",
    "next.js": "https://nextjs.org/learn",
    "node.js": "https://nodejs.org/en/learn",
    "fastapi": "https://fastapi.tiangolo.com/tutorial/",
    "sql": "https://www.postgresql.org/docs/current/tutorial.html",
    "machine learning": "https://scikit-learn.org/stable/tutorial/index.html",
    "deep learning": "https://pytorch.org/tutorials/",
    "nlp": "https://huggingface.co/learn/nlp-course",
    "agentic ai": "https://platform.openai.com/docs/guides/agents",
    "llm": "https://platform.openai.com/docs/guides/text-generation",
    "git": "https://git-scm.com/doc",
    "docker": "https://docs.docker.com/get-started/",
    "html/css": "https://developer.mozilla.org/en-US/docs/Learn_web_development",
    "data analysis": "https://pandas.pydata.org/docs/getting_started/",
    "api design": "https://fastapi.tiangolo.com/tutorial/",
    "testing": "https://docs.pytest.org/en/stable/getting-started.html",
}

INTERVIEW_BANK = {
    "python": [
        {"q": "Explain a Python project you built: what problem did it solve, and what did you personally code?",
         "keywords": ["project", "problem", "code", "built", "function"]},
        {"q": "What is the difference between a list and a tuple in Python, and when would you choose each?",
         "keywords": ["mutable", "immutable", "list", "tuple"]},
        {"q": "How do you handle errors and test a Python function before shipping it?",
         "keywords": ["try", "except", "test", "pytest", "error"]},
    ],
    "machine learning": [
        {"q": "Describe an ML model you trained or used: what data, what metric, and what went wrong first?",
         "keywords": ["data", "model", "metric", "train", "accuracy"]},
        {"q": "How do you detect and reduce overfitting in a model?",
         "keywords": ["overfitting", "validation", "regularization", "data"]},
    ],
    "full-stack": [
        {"q": "Walk through a full-stack feature you shipped: frontend, API, and database — what connected them?",
         "keywords": ["frontend", "api", "database", "feature", "user"]},
        {"q": "How do you debug a bug that only appears in production, not locally?",
         "keywords": ["log", "reproduce", "test", "debug", "production"]},
    ],
    "agentic ai": [
        {"q": "Design a small agent: what tools would it use, what would it never be allowed to do, and how would you check its work?",
         "keywords": ["tool", "check", "verify", "guardrail", "plan"]},
        {"q": "What happens when an agent's tool call fails? How should it recover without inventing an answer?",
         "keywords": ["fail", "retry", "error", "verify", "honest"]},
    ],
}


def _norm(text):
    return " " + re.sub(r"[^a-z0-9+.# ]", " ", (text or "").lower()) + " "


def extract_skills(text):
    """Return skills whose alias appears in text."""
    hay = _norm(text)
    found = []
    for skill, aliases in SKILLS.items():
        if any(a in hay for a in aliases):
            found.append(skill)
    return found


def gap_report(job_description, cv_text, projects):
    """Planner -> Extractor -> GapAnalyser. projects: [{name, link, description}]"""
    required = extract_skills(job_description)
    cv_skills = set(extract_skills(cv_text))
    project_text = " ".join((p.get("name", "") + " " + p.get("description", "") + " " + p.get("link", "")) for p in projects)
    project_skills = set(extract_skills(project_text))
    rows = []
    for skill in required:
        if skill in cv_skills and skill in project_skills:
            status, evidence = "evidenced", "CV + linked project/task supplied"
        elif skill in cv_skills:
            status, evidence = "claimed, not evidenced", "In CV but no linked project/task supplied — add one"
        else:
            status, evidence = "missing", "Not found in CV text supplied"
        rows.append({"skill": skill, "status": status, "evidence": evidence,
                     "task": f"Build one small, shippable project/task using {skill} and link it here."})
    evidenced = sum(1 for r in rows if r["status"] == "evidenced")
    return {"required": required, "rows": rows,
            "summary": f"{evidenced} of {len(rows)} required skills evidenced with a linked project/task."}


def learning_plan(gap, start=None):
    """PlanBuilder: one dated, bite-size task per gap, in order."""
    start = start or date.today()
    plan = []
    day_offset = 0
    for row in gap["rows"]:
        if row["status"] == "evidenced":
            continue
        day = start + timedelta(days=day_offset)
        day_offset += 1
        plan.append({"day": day.isoformat(), "skill": row["skill"], "status": row["status"],
                     "task": row["task"], "resource": RESOURCES.get(row["skill"], ""),
                     "done": False})
    return plan


def portfolio(projects, gap):
    """PortfolioBuilder from real projects only."""
    evidenced = [r["skill"] for r in gap["rows"] if r["status"] == "evidenced"]
    return {"projects": projects,
            "hiring_signal": {"skills_evidenced": evidenced,
                              "projects_shipped": len(projects),
                              "note": "Counts only projects the student supplied. No jobs, employers or certificates are claimed."}}


def interview_questions(role):
    return INTERVIEW_BANK.get(role, INTERVIEW_BANK["python"])


def score_answer(question, answer):
    """Rubric: keyword coverage + evidence + length. Visible, deterministic."""
    text = _norm(answer)
    hits = [k for k in question["keywords"] if k in text]
    coverage = len(hits) / max(1, len(question["keywords"]))
    score = round(min(10, coverage * 8 + (1 if len(answer.split()) >= 40 else 0) + (1 if any(w in text for w in ["project", "built", "example"]) else 0)), 1)
    missing = [k for k in question["keywords"] if k not in text]
    feedback = ("Strong answer — specific and evidenced." if score >= 8 else
                "Good start — add a concrete example from a project you built." if score >= 5 else
                "Add specifics: what you built, what went wrong, and what you measured.")
    if missing:
        feedback += f" Rubric points not yet covered: {', '.join(missing)}."
    return {"score": score, "keywords_hit": hits, "keywords_missing": missing, "feedback": feedback}
