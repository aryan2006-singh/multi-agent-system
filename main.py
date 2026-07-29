"""
main.py
FastAPI backend — chat API + serves the static frontend.
Entry point for `uvicorn main:app`.
"""

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.router import route_query
from config import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("multi_agent_system")

app = FastAPI(title="Multi-Agent Customer Support")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    agents_used: list[str]


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "llm_configured": bool(OPENAI_API_KEY),
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        return ChatResponse(reply="Please type a message.", agents_used=[])

    if not OPENAI_API_KEY:
        return ChatResponse(
            reply=(
                "The server isn't configured with an OpenAI API key yet, "
                "so I can't generate a real reply. Set OPENAI_API_KEY and "
                "try again."
            ),
            agents_used=[],
        )

    try:
        result = route_query(message)
        return ChatResponse(reply=result["reply"], agents_used=result["agents_used"])
    except Exception:
        logger.exception("Failed to handle chat request")
        return ChatResponse(
            reply="Something went wrong while generating a reply. Please try again.",
            agents_used=[],
        )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
