from __future__ import annotations

from pydantic import BaseModel, Field, validator


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

    @validator("message")
    @classmethod
    def validate_message(cls, message: str) -> str:
        cleaned = message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        return cleaned


class ChatResponse(BaseModel):
    answer: str
    model: str
