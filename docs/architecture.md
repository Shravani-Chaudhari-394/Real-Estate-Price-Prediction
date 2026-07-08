# System Architecture

## Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   React     │────▶│   FastAPI    │────▶│  ML Ensemble    │
│  Dashboard  │     │   Backend    │     │  (XGB + NN)     │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌─────────┐ ┌───────────┐
        │PostgreSQL│ │  Redis  │ │ Prometheus│
        └──────────┘ └─────────┘ └─────┬─────┘
                                        ▼
                                  ┌──────────┐
                                  │ Grafana  │
                                  └──────────┘
```

## Components

### Data Pipeline
1. **Collection**: Synthetic data generation simulating 3 APIs + 2 databases
2. **Preprocessing**: StandardScaler for numeric, OneHotEncoder for categorical
3. **Feature Engineering**: Location multipliers, amenity scores, property type encoding

### ML Pipeline
1. **Training**: XGBoost, Neural Network (MLP), and weighted Ensemble
2. **Evaluation**: MAE, MAPE, R² metrics logged to MLflow
3. **Registry**: Model metadata and version tracking in `ml-pipeline/registry/`

### API Layer
- FastAPI with async endpoints
- Prometheus instrumentation (counters, histograms)
- JWT authentication for protected routes
- Pydantic validation on all inputs

### Monitoring
- Prometheus scrapes `/api/v1/prometheus`
- Grafana dashboards for latency, throughput, errors
- Alert rules for high error rate, latency, and downtime

## Data Flow

1. User submits property details via React form
2. FastAPI validates input with Pydantic schemas
3. Prediction service loads ensemble model and generates price
4. Response includes confidence interval and metadata
5. Metrics updated in Prometheus; optional log to PostgreSQL

## Security

- JWT token authentication
- Input validation on all endpoints
- Environment-based secrets management
- GDPR-compliant data handling

## Scalability

- Kubernetes deployment with 3 replicas
- Redis caching for frequent queries
- Horizontal pod autoscaling ready
- Batch endpoint for bulk predictions
