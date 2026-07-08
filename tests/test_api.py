"""Tests for FastAPI endpoints."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.2.0"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "Real Estate" in response.json()["service"]


class TestPredictionEndpoint:
    @patch("backend.api.routes.prediction_service")
    def test_predict_valid_input(self, mock_service):
        from backend.api.schemas import PredictionResponse, ConfidenceInterval

        mock_service.predict.return_value = PredictionResponse(
            prediction_id="test-id",
            timestamp="2026-07-07T00:00:00",
            predicted_price=5000000.0,
            currency="INR",
            confidence_interval=ConfidenceInterval(lower_bound=4500000, upper_bound=5500000),
            model_version="1.2.0",
            metadata={"area_sqft": 1200, "location": "Mumbai", "property_type": "Apartment"},
        )

        response = client.post(
            "/api/v1/predict",
            json={
                "area": 1200,
                "bedrooms": 3,
                "bathrooms": 2,
                "age": 5,
                "location": "Mumbai",
                "property_type": "Apartment",
            },
        )
        assert response.status_code == 200
        assert response.json()["predicted_price"] == 5000000.0

    def test_predict_invalid_area(self):
        response = client.post(
            "/api/v1/predict",
            json={
                "area": -100,
                "bedrooms": 3,
                "bathrooms": 2,
                "age": 5,
                "location": "Mumbai",
                "property_type": "Apartment",
            },
        )
        assert response.status_code == 422


class TestMetricsEndpoint:
    def test_get_metrics(self):
        response = client.get("/api/v1/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_predictions" in data
        assert "model_accuracy_r2" in data


class TestAuthEndpoint:
    def test_login_invalid(self):
        response = client.post("/api/v1/auth/login", json={"username": "bad", "password": "bad"})
        assert response.status_code == 401

    def test_login_valid(self):
        response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
        assert response.status_code == 200
        assert "access_token" in response.json()
