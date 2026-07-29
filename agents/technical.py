"""
technical.py
Technical Support Agent — login issues, password reset,
installation, errors/bugs handle karta hai.
"""

from llm_client import ask_llm
from rag.retriever import retrieve_context

SYSTEM_PROMPT = (
    "Tum ek Technical Support Agent ho. Tumhara kaam hai login issues, "
    "password reset, installation problems, aur bugs/errors solve karna. "
    "Step-by-step troubleshooting instructions do."
)


def handle(query: str) -> str:
    context = retrieve_context(query)
    return ask_llm(SYSTEM_PROMPT, query, context)
