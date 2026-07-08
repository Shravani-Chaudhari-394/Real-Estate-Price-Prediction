"""Tests for ML model training and evaluation."""

import sys
from pathlib import Path

import numpy as np
import pytest
from sklearn.metrics import r2_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ml-pipeline" / "data"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ml-pipeline" / "evaluation"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ml-pipeline" / "training"))

from collector import generate_synthetic_data
from evaluator import evaluate_model
from preprocessor import preprocess_data
from train import EnsembleModel


class TestModelTraining:
    def test_ensemble_model_fit_predict(self):
        df = generate_synthetic_data(200)
        X_train, X_val, _, y_train, y_val, _ = preprocess_data(df)

        model = EnsembleModel()
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)

        assert len(predictions) == len(y_val)
        assert all(p > 0 for p in predictions)

    def test_model_r2_above_threshold(self):
        df = generate_synthetic_data(500)
        X_train, X_val, _, y_train, y_val, _ = preprocess_data(df)

        model = EnsembleModel()
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)
        r2 = r2_score(y_val, predictions)

        assert r2 > 0.5

    def test_evaluate_model_metrics(self):
        y_true = np.array([1000000, 2000000, 3000000])
        y_pred = np.array([1100000, 1900000, 3100000])
        metrics = evaluate_model(y_true, y_pred, "test")

        assert "mae" in metrics
        assert "mape" in metrics
        assert "r2" in metrics
        assert metrics["mae"] > 0
