#!/bin/bash
set -e

echo "=== Real Estate Capstone Setup ==="

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

echo "Training ML models..."
python ml-pipeline/training/train.py

echo "Setup complete. Run: docker-compose up -d"
