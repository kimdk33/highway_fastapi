from typing import cast, Any

from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Config

app = FastAPI(
    title=Config.PROJECT_NAME,
    version=Config.VERSION,
)

app.add_middleware(
    middleware_class=cast(Any, CORSMiddleware),
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hi</h1>"

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": Config.VERSION
        }
