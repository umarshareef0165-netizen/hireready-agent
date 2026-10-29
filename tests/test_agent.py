import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import unittest
from agent import gap_report, learning_plan, portfolio, score_answer, interview_questions

JD = "Python developer: Python, FastAPI, SQL, Docker, testing required."
CV = "Python developer. Built FitTrack in Python with SQL."
PROJ = [{"name": "FitTrack", "link": "https://github.com/example/fittrack", "description": "Python fitness tracker with SQL"}]

class TestHireReady(unittest.TestCase):
    def test_evidenced_only_with_linked_project(self):
        g = gap_report(JD, CV, PROJ)
        by = {r["skill"]: r["status"] for r in g["rows"]}
        self.assertEqual(by["python"], "evidenced")
        self.assertEqual(by["sql"], "evidenced")
    def test_missing_skill(self):
        g = gap_report(JD, CV, PROJ)
        by = {r["skill"]: r["status"] for r in g["rows"]}
        self.assertEqual(by["docker"], "missing")
        self.assertEqual(by["fastapi"], "missing")
    def test_claimed_not_evidenced_without_project(self):
        cv2 = "I know Docker and testing."
        g = gap_report(JD, cv2, [])
        by = {r["skill"]: r["status"] for r in g["rows"]}
        self.assertEqual(by["docker"], "claimed, not evidenced")
    def test_no_fake_evidence(self):
        g = gap_report(JD, "", [])
        self.assertTrue(all(r["status"] == "missing" for r in g["rows"]))
    def test_plan_skips_evidenced(self):
        g = gap_report(JD, CV, PROJ)
        plan = learning_plan(g)
        self.assertTrue(all(p["skill"] not in ("python", "sql") for p in plan))
        self.assertTrue(any(p["skill"] == "docker" for p in plan))
        self.assertTrue(all(p["day"] and p["resource"] for p in plan))
    def test_portfolio_counts_only_supplied(self):
        g = gap_report(JD, CV, PROJ)
        p = portfolio(PROJ, g)
        self.assertEqual(p["hiring_signal"]["projects_shipped"], 1)
        self.assertIn("python", p["hiring_signal"]["skills_evidenced"])
    def test_interview_scoring_visible_rubric(self):
        q = interview_questions("python")[1]
        good = score_answer(q, "A list is mutable and a tuple is immutable, so I use a list when data changes and a tuple for fixed config.")
        bad = score_answer(q, "I don't know.")
        self.assertGreater(good["score"], bad["score"])
        self.assertIn("mutable", good["keywords_hit"])
    def test_interview_questions_exist_for_all_roles(self):
        for role in ("python", "machine learning", "full-stack", "agentic ai"):
            self.assertGreaterEqual(len(interview_questions(role)), 2)
    def test_empty_inputs_do_not_crash(self):
        g = gap_report("", "", [])
        self.assertEqual(g["rows"], [])

if __name__ == "__main__":
    unittest.main()
