# MediVision AI FastAPI Backend

## Structure

```text
backend/
  app/
    api/routes.py              # FastAPI endpoints
    core/config.py             # Paths and environment settings
    schemas/                   # Pydantic request/response models
    services/                  # Disease model and chatbot logic
    main.py                    # FastAPI app factory
  main.py                      # Compatibility entrypoint
  requirements.txt
```

Start the API from the repository root:

```powershell
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Set your real Gemini key in `backend/.env`:

```text
GEMINI_API_KEY="your-gemini-api-key"
GEMINI_MODEL="gemini-1.5-flash"
GEMINI_TEMPERATURE="0.3"
GEMINI_MAX_OUTPUT_TOKENS="1024"
```

You can also run the app package directly:

```powershell
uvicorn backend.app.main:app --reload
```

The Disease Prediction page calls `POST http://localhost:8000/predict` with one to five symptoms:

```json
{
  "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic _patches", "fatigue"]
}
```

Use `GET http://localhost:8000/symptoms` to list valid symptom names.

The Health Chatbot page calls `POST http://localhost:8000/chat`:

```json
{
  "message": "What are common cold symptoms?"
}
```

Set `GOOGLE_API_KEY` or `GEMINI_API_KEY` in `backend/.env` before starting FastAPI. This is the only env file loaded by the backend, and it is ignored by git.

Model-related environment variables can also be set in `backend/.env`, including Gemini settings and disease model file paths.
