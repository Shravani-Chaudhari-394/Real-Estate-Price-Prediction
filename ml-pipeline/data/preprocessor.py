"""Data preprocessing and feature engineering."""

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logger = logging.getLogger(__name__)

NUMERIC_FEATURES = ["area", "bedrooms", "bathrooms", "age", "floor", "amenities_score"]
CATEGORICAL_FEATURES = ["location", "property_type", "facing"]


def create_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )


def preprocess_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42,
):
    """Split and preprocess data for training."""
    X = df.drop("price", axis=1)
    y = df["price"]

    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_ratio, random_state=random_state
    )

    logger.info("Data split: train=%d, val=%d, test=%d", len(X_train), len(X_val), len(X_test))
    return X_train, X_val, X_test, y_train, y_val, y_test


def save_processed_data(output_dir: str | Path, df: pd.DataFrame) -> None:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(path / "processed_data.csv", index=False)
    joblib.dump(create_preprocessor(), path / "preprocessor.pkl")
    logger.info("Processed data saved to %s", path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from collector import collect_data

    base = Path(__file__).resolve().parent
    raw_path = base / "raw" / "real_estate_data.csv"
    if not raw_path.exists():
        collect_data(raw_path)
    df = pd.read_csv(raw_path)
    save_processed_data(base / "processed", df)
