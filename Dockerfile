FROM python:3.8-alpine AS base

# Maintainer
LABEL maintainer="Linka González <linkag@protonmail.ch>"

# We need gcc to build some python libraries
RUN apk add build-base

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Ports
ENV     CONTAINER_PORT=5000 \
        BIND_INTERFACE=0.0.0.0 \
        GRACEFUL_TIMEOUT=300 \
        TIMEOUT=300 \
        WORKER_CONNECTIONS=10 \
        WORKERS=3 \
        SOURCES_PATH=./data/sources.json.example \
        DATABASE_URL=sqlite:///./default.db

EXPOSE ${CONTAINER_PORT}

# Setup Database

RUN alembic upgrade head

# run gunicorn
CMD ["sh", "-c", "gunicorn --bind ${BIND_INTERFACE}:${CONTAINER_PORT} --graceful-timeout ${GRACEFUL_TIMEOUT} --timeout ${TIMEOUT} --worker-class=uvicorn.workers.UvicornWorker --worker-connections ${WORKER_CONNECTIONS} --workers ${WORKERS} wsgi-service:app"]

