"""
rag/retriever.py
Halka-fulka (lightweight) local RAG retriever. Company documents
data/*.md se load hote hain aur simple keyword-overlap scoring se
sabse relevant paragraphs return kiye jaate hain.

Koi external vector DB / embeddings API nahi use kiya — isse
deploy simple rehta hai (Render free tier pe bhi chalega) aur koi
extra cost nahi lagti. Baad mein isse embeddings-based search se
upgrade kiya ja sakta hai.
"""

import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "to", "of", "in", "on",
    "for", "and", "or", "how", "what", "why", "do", "does", "i", "my",
    "hai", "ka", "ki", "ke", "kya", "kaise", "mera", "mujhe", "se", "me",
}


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def _load_paragraphs() -> list[str]:
    paragraphs = []
    if not DATA_DIR.exists():
        return paragraphs
    for path in sorted(DATA_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for block in text.split("\n\n"):
            block = block.strip()
            if block:
                paragraphs.append(block)
    return paragraphs


_PARAGRAPHS = _load_paragraphs()


def retrieve_context(query: str, top_k: int = 3) -> str:
    """
    Query se sabse relevant top_k paragraphs dhoondh ke ek single
    string mein joda hua context return karta hai. Kuch relevant
    na mile to empty string return hoti hai.
    """
    if not _PARAGRAPHS:
        return ""

    query_tokens = _tokenize(query)
    if not query_tokens:
        return ""

    scored = []
    for paragraph in _PARAGRAPHS:
        para_tokens = _tokenize(paragraph)
        overlap = len(query_tokens & para_tokens)
        if overlap > 0:
            scored.append((overlap, paragraph))

    scored.sort(key=lambda item: item[0], reverse=True)
    top = [paragraph for _, paragraph in scored[:top_k]]
    return "\n\n".join(top)
