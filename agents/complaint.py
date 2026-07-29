"""
complaint.py
Complaint Agent — unhappy customers, escalations handle karta hai.
Empathy zaroori hai is agent mein.
"""

from llm_client import ask_llm
from rag.retriever import retrieve_context

SYSTEM_PROMPT = (
    "Tum ek Complaint Resolution Agent ho. Customer frustrated ho sakta "
    "hai — pehle empathy dikhao, phir solution ya next steps batao. "
    "Agar zaroori ho to human escalation suggest karo."
)


def handle(query: str) -> str:
    context = retrieve_context(query)
    return ask_llm(SYSTEM_PROMPT, query, context)
