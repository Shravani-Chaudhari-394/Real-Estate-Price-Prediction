# User Manual

## Getting Started

1. Open the dashboard at http://localhost:3000
2. Use the **Predict** tab to estimate property prices
3. Use the **Dashboard** tab to view system metrics and feature importance

## Making a Prediction

1. Enter property details:
   - **Area**: Square footage (400–5000)
   - **Bedrooms/Bathrooms**: Room counts
   - **Age**: Property age in years
   - **Location**: City (Mumbai, Delhi, Bangalore, etc.)
   - **Property Type**: Apartment, Villa, Penthouse, Studio, Duplex

2. Click **Predict Price**
3. View the predicted price and confidence interval

## Understanding Results

- **Predicted Price**: Model's best estimate in INR
- **Confidence Interval**: ±10% range around the prediction
- **Model Version**: Current production model version

## Dashboard Metrics

| Metric | Description |
|--------|-------------|
| Total Predictions | Cumulative predictions served |
| Avg Latency | Mean API response time |
| Error Rate | Percentage of failed predictions |
| Model R² | Model accuracy score |
| API Availability | Uptime percentage |
| Data Freshness | Hours since last data refresh |

## Authentication

For protected endpoints, login via API:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Use the returned `access_token` in subsequent requests:
```
Authorization: Bearer <token>
```

## Maintenance

- Retrain models monthly: `python ml-pipeline/training/train.py`
- Check system status: `python scripts/system_status.py`
- View logs: `docker-compose logs -f backend`
