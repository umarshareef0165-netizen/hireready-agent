"""Real-LLM adapter STUB — NOT wired into server.py.

To go live: implement call_llm(prompt) reading its key from the environment
only (never committed, never printed), run ONE live gap-report comparison
against the deterministic mock, and only then wire it behind a flag.
Until then every claim about the app must say 'mock mode'.
No key, token or endpoint is claimed here.
"""
import os

def call_llm(prompt):
    key = os.environ.get("HIREREADY_LLM_KEY")
    if not key:
        raise RuntimeError("HIREREADY_LLM_KEY is not set; mock mode must be used instead.")
    raise NotImplementedError("Live LLM provider not yet configured — do not claim live AI until this is implemented and tested.")
