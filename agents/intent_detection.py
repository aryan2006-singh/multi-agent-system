"""
intent_detection.py
Ye module decide karta hai ki customer ki query kis category
(ya categories) mein aati hai. LLM ko hi classifier ki tarah
use kar rahe hain — ye chhote projects ke liye simple aur
effective approach hai (baad mein Banking77 dataset se apna
khud ka classifier bhi train kar sakte ho).
"""

from llm_client import ask_llm

CATEGORIES = ["billing", "technical", "product", "complaint", "faq"]

SYSTEM_PROMPT = (
    "Tum ek intent classifier ho. Customer ki query padh ke, ye batao "
    "ki kaunsi categories relevant hain in mein se: billing, technical, "
    "product, complaint, faq. Ek query ek se zyada categories mein bhi "
    "aa sakti hai (jaise billing + technical). "
    "SIRF category names comma-separated return karo, kuch aur text mat likho. "
    "Example output: billing,technical"
)


def detect_intent(query: str) -> list[str]:
    raw_response = ask_llm(SYSTEM_PROMPT, query)
    detected = [c.strip().lower() for c in raw_response.split(",")]
    # Sirf valid categories hi rakho, agar LLM ne kuch galat likh diya to ignore
    valid = [c for c in detected if c in CATEGORIES]
    return valid if valid else ["faq"]   # kuch na mile to default FAQ agent
