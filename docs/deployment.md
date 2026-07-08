# Deployment Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- 4GB RAM minimum

## Local Development

```bash
# 1. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Train the model
python ml-pipeline/training/train.py

# 3. Start backend
uvicorn backend.main:app --reload --port 8000

# 4. Start frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Docker Deployment

```bash
# Train model first (saves to backend/models/)
python ml-pipeline/training/train.py

# Start all services
docker-compose up -d

# Check status
docker-compose ps
curl http://localhost:8000/api/v1/health
```

## Kubernetes Deployment

```bash
# Build and push images
docker build -f infrastructure/docker/Dockerfile.backend -t real-estate-api:1.2.0 .
docker build -f infrastructure/docker/Dockerfile.frontend -t real-estate-frontend:1.2.0 .

# Apply manifests
kubectl apply -f infrastructure/kubernetes/deployment.yaml
```

## Environment Variables

| Variable       | Default              | Description          |
|----------------|----------------------|----------------------|
| DATABASE_URL   | sqlite:///./real_estate.db | Database connection |
| REDIS_URL      | redis://localhost:6379 | Redis cache URL    |
| SECRET_KEY     | (dev default)        | JWT signing key      |

## Monitoring Setup

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)
- API metrics: http://localhost:8000/api/v1/prometheus

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Run `python ml-pipeline/training/train.py` |
| Port 8000 in use | Change port: `uvicorn backend.main:app --port 8001` |
| Frontend can't reach API | Check `VITE_API_URL` env var |
| Docker build fails | Ensure model is trained before `docker-compose up` |
