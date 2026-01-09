# src/api/main.py

from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="AI Marketing Intelligence API",
    version="1.0.0",
    description="Agentic AI system for customer behavior analysis and campaign recommendations",
)

app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "ok"}
