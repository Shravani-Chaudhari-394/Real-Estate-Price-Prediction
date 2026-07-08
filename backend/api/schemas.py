"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PropertyRequest(BaseModel):
    area: float = Field(..., gt=0, description="Area in square feet")
    bedrooms: int = Field(..., ge=1, le=10)
    bathrooms: int = Field(..., ge=1, le=10)
    age: int = Field(..., ge=0, le=100)
    location: str
    property_type: str
    floor: int = Field(default=1, ge=0)
    facing: str = "East"
    amenities_score: float = Field(default=5.0, ge=1, le=10)


class ConfidenceInterval(BaseModel):
    lower_bound: float
    upper_bound: float


class PredictionResponse(BaseModel):
    prediction_id: str
    timestamp: str
    predicted_price: float
    currency: str = "INR"
    confidence_interval: ConfidenceInterval
    model_version: str
    metadata: dict


class BatchPropertyRequest(BaseModel):
    properties: list[PropertyRequest]


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]
    total: int
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    model_loaded: bool
    timestamp: str


class MetricsResponse(BaseModel):
    total_predictions: int
    average_latency_ms: float
    error_rate: float
    model_accuracy_r2: float
    api_availability: float
    data_freshness_hours: int


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
