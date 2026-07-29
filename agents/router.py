"""
router.py
Ye "orchestrator" hai — sabse zaroori piece.
1. Intent detect karta hai
2. Un intents ke corresponding agents ko call karta hai
3. Agar multiple agents involved hain, unke jawab combine karta hai

Example: "maine kal payment kiya par premium lock hai" ->
intent = [billing, technical] -> dono agents call honge -> combined jawab
"""

from agents.intent_detection import detect_intent
from agents import billing, technical, product, complaint, faq

AGENT_MAP = {
    "billing": billing.handle,
    "technical": technical.handle,
    "product": product.handle,
    "complaint": complaint.handle,
    "faq": faq.handle,
}


def route_query(query: str) -> dict:
    """
    Return karta hai: {"reply": "...", "agents_used": [...]}
    """
    intents = detect_intent(query)

    responses = []
    for intent in intents:
        handler = AGENT_MAP.get(intent)
        if handler:
            responses.append(f"({intent.upper()} AGENT): {handler(query)}")

    # Agar ek se zyada agent involved hain, unke jawab ko jodo.
    # (Response Aggregator step — jaisa architecture diagram mein tha)
    final_reply = "\n\n".join(responses)

    return {"reply": final_reply, "agents_used": intents}
