# A small, dependency-free deployment image for SafeRoute AI.
FROM python:3.12-slim

WORKDIR /app
COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8001

CMD ["python", "backend/server.py"]
