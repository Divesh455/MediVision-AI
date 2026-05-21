from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import HTTPException

from backend.app.core.config import (
    GEMINI_MAX_OUTPUT_TOKENS,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    get_gemini_api_key,
)
from backend.app.schemas.chat import ChatRequest, ChatResponse


SYSTEM_PROMPT = (
    "You are MediAI Assistant, a careful and concise health information assistant. "
    "Answer general health, symptom, wellness, and medication-information questions "
    "in clear language. Do not diagnose the user or claim certainty. Encourage urgent "
    "medical care for emergency symptoms and recommend consulting a qualified healthcare "
    "professional for diagnosis, treatment, medication changes, or personalized advice."
)


@lru_cache(maxsize=1)
def get_chat_model() -> Any:
    api_key = get_gemini_api_key()
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured. Set GOOGLE_API_KEY or GEMINI_API_KEY.",
        )

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="LangChain Gemini dependency is missing. Run: pip install -r backend/requirements.txt",
        ) from exc

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        temperature=GEMINI_TEMPERATURE,
        max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
    )


def get_chat_response(payload: ChatRequest) -> ChatResponse:
    try:
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="LangChain dependency is missing. Run: pip install -r backend/requirements.txt",
        ) from exc

    chat_model = get_chat_model()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=payload.message),
    ]

    try:
        response = chat_model.invoke(messages)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini request failed: {exc}") from exc

    return ChatResponse(answer=str(response.content), model=GEMINI_MODEL)
