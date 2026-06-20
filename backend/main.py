"""
FastAPI entrypoint for MediAI.

Run this from the project root:
    uvicorn backend.main:app --reload

The full app setup lives in backend/app/main.py so routes, schemas,
services, and config can stay organized in separate modules.
"""

from backend.app.main import app, create_app

__all__ = ["app", "create_app"]
