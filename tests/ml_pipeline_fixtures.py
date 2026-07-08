"""Shared test fixtures."""

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE / "backend" / "models" / "production_model.pkl"


def ensure_model_trained():
    if not MODEL_PATH.exists():
        subprocess.run([sys.executable, str(BASE / "ml-pipeline" / "training" / "train.py")], check=True)
