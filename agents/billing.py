"""
billing.py
Billing Agent — payments, subscription, invoice, refund se
related sawaalon ko handle karta hai.
"""

from llm_client import ask_llm
from rag.retriever import retrieve_context

SYSTEM_PROMPT = (
    "Tum ek Billing Support Agent ho. Tumhara kaam hai customers ke "
    "payment, subscription, invoice, aur refund se related sawaalon "
    "ka madad karna. Polite aur clear jawab do."
)


def handle(query: str) -> str:
    context = retrieve_context(query)
    return ask_llm(SYSTEM_PROMPT, query, context)
