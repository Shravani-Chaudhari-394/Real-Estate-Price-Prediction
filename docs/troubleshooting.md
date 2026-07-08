# Troubleshooting Guide

## Common Issues

### Model Not Found (500 error on predict)

**Symptom:** API returns 500 with "Model not loaded"

**Fix:**
```bash
python ml-pipeline/training/train.py
# Verify model exists
ls backend/models/production_model.pkl
```

### High Latency

**Symptom:** Predictions taking >500ms

**Checks:**
1. Check Redis cache connectivity
2. Review Prometheus latency histogram
3. Ensure model file is on local disk (not network mount)

### Authentication Failures

**Symptom:** 401 on protected endpoints

**Fix:** Login to get a fresh token:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Docker Services Not Starting

```bash
docker-compose down
docker-compose up -d --build
docker-compose logs backend
```

### Frontend Cannot Connect to API

1. Verify backend is running: `curl http://localhost:8000/api/v1/health`
2. Check CORS settings in `backend/main.py`
3. Set `VITE_API_URL=http://localhost:8000` in frontend `.env`

### Test Failures

```bash
pip install -r requirements.txt
python ml-pipeline/training/train.py
pytest tests/ -v
```

### Model Drift Detection

Monitor these signals:
- Increasing MAE in production predictions
- R² dropping below 0.80 on validation set
- Feature distribution shifts in input data

Retrain when drift is detected.
