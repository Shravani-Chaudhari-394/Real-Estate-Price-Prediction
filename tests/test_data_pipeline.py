"""Tests for data collection and preprocessing."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ml-pipeline" / "data"))

from collector import generate_synthetic_data, LOCATIONS, PROPERTY_TYPES
from preprocessor import create_preprocessor, preprocess_data


class TestDataCollection:
    def test_generate_synthetic_data_shape(self):
        df = generate_synthetic_data(100)
        assert len(df) == 100
        assert "price" in df.columns
        assert "area" in df.columns

    def test_price_positive(self):
        df = generate_synthetic_data(50)
        assert (df["price"] > 0).all()

    def test_valid_locations(self):
        df = generate_synthetic_data(100)
        assert set(df["location"].unique()).issubset(set(LOCATIONS))

    def test_valid_property_types(self):
        df = generate_synthetic_data(100)
        assert set(df["property_type"].unique()).issubset(set(PROPERTY_TYPES))


class TestPreprocessor:
    def test_create_preprocessor(self):
        preprocessor = create_preprocessor()
        assert preprocessor is not None

    def test_data_split(self):
        df = generate_synthetic_data(200)
        X_train, X_val, X_test, y_train, y_val, y_test = preprocess_data(df)
        assert len(X_train) > 0
        assert len(X_val) > 0
        assert len(X_test) > 0
        total = len(X_train) + len(X_val) + len(X_test)
        assert total == 200

    def test_preprocessor_fit_transform(self):
        df = generate_synthetic_data(50)
        X = df.drop("price", axis=1)
        preprocessor = create_preprocessor()
        result = preprocessor.fit_transform(X)
        assert result.shape[0] == 50
