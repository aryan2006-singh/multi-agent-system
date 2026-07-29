"""
faq.py
FAQ Agent — general questions, company policies, contact info
jaise generic sawaal handle karta hai.
"""

from llm_client import ask_llm
from rag.retriever import retrieve_context

SYSTEM_PROMPT = (
    "Tum ek General FAQ Agent ho. Company policies, general questions, "
    "aur contact information se related sawaalon ke jawab do."
)


def handle(query: str) -> str:
    context = retrieve_context(query)
    return ask_llm(SYSTEM_PROMPT, query, context)
