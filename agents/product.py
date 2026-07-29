"""
product.py
Product Agent — features, pricing, comparisons, availability
se related sawaal handle karta hai.
"""

from llm_client import ask_llm
from rag.retriever import retrieve_context

SYSTEM_PROMPT = (
    "Tum ek Product Information Agent ho. Tumhara kaam hai product "
    "features, pricing, comparisons, aur availability ke baare mein "
    "accurate info dena."
)


def handle(query: str) -> str:
    context = retrieve_context(query)
    return ask_llm(SYSTEM_PROMPT, query, context)
