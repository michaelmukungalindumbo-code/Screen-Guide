from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.knowledge import find_local_match

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ALLOWED_ORIGINS == ["*"] else settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswerRequest(BaseModel):
    question: str


@app.get("/health")
def healthcheck():
    return {"status": "ok", "service": settings.APP_NAME}


@app.post("/api/answer")
def answer_question(payload: AnswerRequest):
    question = payload.question.strip()

    if not question:
        return {"question": question, "answer": "Please provide a valid question.", "source": "validation"}

    local_answer = find_local_match(question)
    if local_answer:
        return {"question": question, "answer": local_answer, "source": "local-match"}

    if not settings.OPENAI_API_KEY or OpenAI is None:
        return {
            "question": question,
            "answer": "I don't have a guide for that yet. This app needs an AI service to answer open-ended questions like this.",
            "source": "not-configured",
        }

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": (
                    "You are a helpful assistant for a user of a guide-based app. "
                    "Answer the user's question clearly, practically, and concisely. "
                    f"Question: {question}"
                ),
            }
        ],
        temperature=0.3,
        max_output_tokens=500,
    )

    answer = response.output_text.strip() if getattr(response, "output_text", None) else "I couldn't generate a response right now."
    return {"question": question, "answer": answer, "source": "llm"}
