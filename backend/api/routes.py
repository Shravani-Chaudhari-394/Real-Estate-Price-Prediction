"""API route handlers."""

import time
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

from backend.api.schemas import (
    PropertyRequest,
    PredictionResponse,
    BatchPropertyRequest,
    BatchPredictionResponse,
    HealthResponse,
    MetricsResponse,
    LoginRequest,
    TokenResponse,
)
from backend.services.prediction_service import PredictionService
from backend.services.auth_service import authenticate_user, create_access_token, get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")
prediction_service = PredictionService()

PREDICTION_COUNTER = Counter("predictions_total", "Total predictions made")
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency")
ERROR_COUNTER = Counter("prediction_errors_total", "Total prediction errors")

_start_time = datetime.now()


@router.post("/predict", response_model=PredictionResponse)
def predict_price(request: PropertyRequest):
    with PREDICTION_LATENCY.time():
        try:
            PREDICTION_COUNTER.inc()
            if request.area <= 0:
                raise HTTPException(status_code=400, detail="Area must be positive")
            return prediction_service.predict(request)
        except HTTPException:
            raise
        except Exception as e:
            ERROR_COUNTER.inc()
            logger.error("Prediction error: %s", str(e))
            raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/batch", response_model=BatchPredictionResponse)
def batch_predict(request: BatchPropertyRequest):
    start = time.time()
    predictions = []
    for prop in request.properties:
        try:
            predictions.append(prediction_service.predict(prop))
            PREDICTION_COUNTER.inc()
        except Exception as e:
            ERROR_COUNTER.inc()
            logger.error("Batch prediction error: %s", str(e))

    elapsed = (time.time() - start) * 1000
    return BatchPredictionResponse(
        predictions=predictions,
        total=len(predictions),
        processing_time_ms=round(elapsed, 1),
    )


@router.get("/health", response_model=HealthResponse)
def health_check():
    uptime = (datetime.now() - _start_time).total_seconds()
    return HealthResponse(
        status="healthy",
        version="1.2.0",
        uptime_seconds=round(uptime, 1),
        model_loaded=prediction_service.is_model_loaded(),
        timestamp=datetime.now().isoformat(),
    )


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    m = prediction_service.get_metrics()
    return MetricsResponse(**m)


@router.get("/prometheus")
def prometheus_metrics():
    return Response(content=generate_latest(), media_type="text/plain")


@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return TokenResponse(access_token=token)


@router.get("/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
