"""Integration tests for prediction service and database."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.api.schemas import PropertyRequest
from backend.services.prediction_service import PredictionService
from backend.services.auth_service import authenticate_user, create_access_token, get_current_user
from backend.database.models import init_db, PredictionLog, Base, engine
from backend.models.ml_system import RealEstateMLSystem
from ml_pipeline_fixtures import ensure_model_trained


@pytest.fixture(scope="module", autouse=True)
def setup():
    ensure_model_trained()
    init_db()


class TestPredictionService:
    def setup_method(self):
        self.service = PredictionService()

    def test_model_loaded(self):
        assert self.service.is_model_loaded()

    def test_predict_returns_valid_response(self):
        request = PropertyRequest(
            area=1200,
            bedrooms=3,
            bathrooms=2,
            age=5,
            location="Mumbai",
            property_type="Apartment",
        )
        result = self.service.predict(request)
        assert result.predicted_price > 0
        assert result.currency == "INR"
        assert result.confidence_interval.lower_bound < result.predicted_price

    def test_metrics_after_prediction(self):
        request = PropertyRequest(
            area=1000,
            bedrooms=2,
            bathrooms=1,
            age=10,
            location="Pune",
            property_type="Apartment",
        )
        self.service.predict(request)
        metrics = self.service.get_metrics()
        assert metrics["total_predictions"] >= 1
        assert metrics["model_accuracy_r2"] > 0


class TestAuthService:
    def test_authenticate_valid_user(self):
        user = authenticate_user("admin", "admin123")
        assert user is not None
        assert user["role"] == "admin"

    def test_authenticate_invalid_user(self):
        assert authenticate_user("admin", "wrong") is None

    def test_create_token(self):
        token = create_access_token({"sub": "admin"})
        assert isinstance(token, str)
        assert len(token) > 0


class TestDatabase:
    def test_init_db(self):
        init_db()
        assert PredictionLog.__tablename__ == "prediction_logs"

    def test_tables_created(self):
        tables = Base.metadata.tables.keys()
        assert "prediction_logs" in tables


class TestMLSystem:
    def test_build_pipeline(self):
        system = RealEstateMLSystem()
        system.build_pipeline()
        assert system.pipeline is not None

    def test_load_model(self):
        model_path = Path(__file__).resolve().parent.parent / "backend" / "models" / "production_model.pkl"
        if model_path.exists():
            system = RealEstateMLSystem(model_path=model_path)
            system.load_model()
            assert system.pipeline is not None
