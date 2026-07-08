"""FastAPI application entry point."""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.api.routes import router
from backend.database.models import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Real Estate Price Predictor",
    description="Production-ready ML system for real estate price prediction",
    version="1.2.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    init_db()
    logging.getLogger(__name__).info("Real Estate Price Prediction API started")


@app.get("/")
async def root():
    return {
        "service": "Real Estate Price Prediction System",
        "version": "1.2.0",
        "docs": "/api/v1/docs",
        "health": "/api/v1/health",
    }
