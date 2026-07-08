# Contributing

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Train the model: `python ml-pipeline/training/train.py`
5. Start services: `docker-compose up -d`

## Code Style

- Python: PEP 8, type hints where practical
- TypeScript/React: ESLint configuration in `frontend/`
- Run tests before submitting: `pytest tests/ -v --cov`

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass and coverage stays above 80%
5. Update documentation as needed
6. Submit a pull request with a clear description
