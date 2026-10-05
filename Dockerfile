FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app
COPY src/ ./src/
COPY tests/ ./tests/
USER 1000:1000

CMD ["python", "tests/check_portfolio_snapshot.py"]
