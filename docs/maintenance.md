# Maintenance Guide

## Regular Tasks

| Task | Frequency | Command |
|------|-----------|---------|
| Retrain models | Monthly | `python ml-pipeline/training/train.py` |
| Check system status | Weekly | `python scripts/system_status.py` |
| Review metrics | Daily | Visit Grafana dashboard |
| Database backup | Daily | Automated via Docker volume |
| Dependency updates | Monthly | `pip install -r requirements.txt --upgrade` |

## Model Retraining

1. Collect fresh data: `python ml-pipeline/data/collector.py`
2. Train models: `python ml-pipeline/training/train.py`
3. Review evaluation report in `ml-pipeline/registry/evaluation_report.json`
4. Restart backend: `docker-compose restart backend`

## Monitoring Checks

- Prometheus targets should all be UP
- Error rate should stay below 1%
- P95 latency should stay below 500ms
- Model R² should not drop below 0.80

## Log Rotation

Application logs are written to stdout. In Docker, use:
```bash
docker-compose logs --tail=100 backend
```

## Scaling

To scale API replicas in Kubernetes:
```bash
kubectl scale deployment real-estate-api --replicas=5
```
