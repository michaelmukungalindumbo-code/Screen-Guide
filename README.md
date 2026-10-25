# Screen Guide

Screen Guide is a mobile app project that currently appears to be built around static guide content and keyword matching. This repository now includes an experimental AI backend layer so the app can answer broader, open-ended questions such as "How do I upload content on YouTube?" when the user asks outside the built-in guide set.

## Included

- `backend/` — small FastAPI service that exposes a single AI answer endpoint
- `backend/.env.example` — environment variables for the model service
- `backend/README.md` — quick-start instructions

## Architecture

- Android app: static local guide lookup
- AI service: backend endpoint for open-ended questions
- App integration: the mobile app can call the backend when a local guide match is missing

## Backend quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then call:

```bash
curl -X POST http://localhost:8000/api/answer \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I upload content on YouTube?"}'
```

## Notes

This is intentionally a small, modular layer. It does not replace the Android app. It adds an AI fallback so the app can answer questions beyond its packaged guides.
