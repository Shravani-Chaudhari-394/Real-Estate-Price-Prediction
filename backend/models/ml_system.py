"""Real Estate ML System - production ML pipeline wrapper."""

import logging
from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

logger = logging.getLogger(__name__)


class RealEstateMLSystem:
    def __init__(self, model_path: str | Path | None = None):
        self.pipeline = None
        self.metrics: dict = {}
        self.logger = logging.getLogger(__name__)
        self.model_path = Path(model_path) if model_path else None

    def build_pipeline(self):
        import sys

        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "ml-pipeline" / "data"))
        from preprocessor import create_preprocessor

        self.pipeline = Pipeline(
            [
                ("preprocessor", create_preprocessor()),
                (
                    "model",
                    XGBRegressor(
                        n_estimators=200,
                        learning_rate=0.1,
                        max_depth=6,
                        random_state=42,
                    ),
                ),
            ]
        )

    def train_with_tracking(self, X_train, y_train, X_val, y_val):
        if self.pipeline is None:
            self.build_pipeline()

        mlflow.set_experiment("real_estate_pricing")
        with mlflow.start_run():
            mlflow.log_params(self.pipeline.named_steps["model"].get_params())

            self.pipeline.fit(X_train, y_train)

            train_pred = self.pipeline.predict(X_train)
            val_pred = self.pipeline.predict(X_val)

            train_mae = mean_absolute_error(y_train, train_pred)
            val_mae = mean_absolute_error(y_val, val_pred)
            val_r2 = r2_score(y_val, val_pred)

            mlflow.log_metrics({"train_mae": train_mae, "val_mae": val_mae, "val_r2": val_r2})
            mlflow.sklearn.log_model(self.pipeline, "model")

            self.metrics = {"train_mae": train_mae, "val_mae": val_mae, "val_r2": val_r2}
            self.logger.info("Training complete. Validation MAE: ₹%s, R²: %.3f", f"{val_mae:,.2f}", val_r2)
            return self.metrics

    def load_model(self, path: str | Path | None = None):
        load_path = Path(path) if path else self.model_path
        if load_path and load_path.exists():
            self.pipeline = joblib.load(load_path)
            self.logger.info("Model loaded from %s", load_path)
        else:
            raise FileNotFoundError(f"Model not found at {load_path}")

    def predict(self, input_data: pd.DataFrame) -> float:
        if self.pipeline is None:
            self.load_model()
        return float(self.pipeline.predict(input_data)[0])
