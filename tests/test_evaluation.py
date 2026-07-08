"""Tests for evaluation and collector modules."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ml-pipeline" / "data"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ml-pipeline" / "evaluation"))

from collector import collect_data, generate_synthetic_data
from evaluator import evaluate_model, get_feature_importance, save_evaluation_report
from preprocessor import save_processed_data


class TestCollectorModule:
    def test_collect_data_with_output(self, tmp_path):
        output = tmp_path / "data.csv"
        df = collect_data(output, n_samples=50)
        assert output.exists()
        assert len(df) == 50


class TestEvaluatorModule:
    def test_feature_importance(self):
        class MockModel:
            feature_importances_ = np.array([0.5, 0.3, 0.2])

        result = get_feature_importance(MockModel(), ["a", "b", "c"], top_n=2)
        assert len(result) == 2
        assert result[0]["feature"] == "a"

    def test_save_report(self, tmp_path):
        save_evaluation_report({"mae": 100}, tmp_path / "report.json")
        assert (tmp_path / "report.json").exists()


class TestPreprocessorModule:
    def test_save_processed(self, tmp_path):
        df = generate_synthetic_data(100)
        save_processed_data(tmp_path, df)
        assert (tmp_path / "processed_data.csv").exists()
        assert (tmp_path / "preprocessor.pkl").exists()
