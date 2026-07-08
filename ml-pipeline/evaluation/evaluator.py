"""Model evaluation utilities."""

import json
import logging
from pathlib import Path

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

logger = logging.getLogger(__name__)


def evaluate_model(y_true, y_pred, model_name: str = "model") -> dict:
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    r2 = r2_score(y_true, y_pred)

    metrics = {
        "model": model_name,
        "mae": round(mae, 2),
        "mape": round(mape, 2),
        "r2": round(r2, 4),
    }
    logger.info("%s - MAE: ₹%s, MAPE: %.1f%%, R²: %.3f", model_name, f"{mae:,.0f}", mape, r2)
    return metrics


def get_feature_importance(model, feature_names: list[str], top_n: int = 5) -> list[dict]:
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    total = importances.sum()
    return [
        {"feature": feature_names[i], "importance": round(importances[i] / total * 100, 1)}
        for i in indices
    ]


def save_evaluation_report(metrics: dict, output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info("Evaluation report saved to %s", path)
