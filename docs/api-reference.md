# API Reference

Base URL: `http://localhost:8000`

## POST /api/v1/predict

Predict property price from features.

**Request Body:**
```json
{
  "area": 1200,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "location": "Mumbai",
  "property_type": "Apartment",
  "floor": 5,
  "facing": "East",
  "amenities_score": 7.0
}
```

**Response (200):**
```json
{
  "prediction_id": "uuid",
  "timestamp": "2026-07-07T00:00:00",
  "predicted_price": 12500000.0,
  "currency": "INR",
  "confidence_interval": {
    "lower_bound": 11250000.0,
    "upper_bound": 13750000.0
  },
  "model_version": "1.2.0",
  "metadata": {
    "area_sqft": 1200,
    "location": "Mumbai",
    "property_type": "Apartment"
  }
}
```

## POST /api/v1/batch

Batch predictions for multiple properties.

**Request:** `{ "properties": [ {...}, {...} ] }`

## GET /api/v1/health

Returns system health status.

## GET /api/v1/metrics

Returns performance metrics (predictions, latency, error rate, R²).

## POST /api/v1/auth/login

Authenticate and receive JWT token.

**Request:** `{ "username": "admin", "password": "admin123" }`

## GET /api/v1/prometheus

Prometheus-format metrics for scraping.

## Error Codes

| Code | Description |
|------|-------------|
| 400  | Invalid input (e.g., negative area) |
| 401  | Authentication failed |
| 422  | Validation error |
| 500  | Internal server error |
