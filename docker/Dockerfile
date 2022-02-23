FROM python:3.8-alpine AS base

# Maintainer
LABEL maintainer="Pablo Santa Cruz <pablo@roshka.com.py>"

# We need gcc to build some python libraries
RUN apk add build-base

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy startup script
COPY docker/startup.sh .

# Copy application
COPY . .

# Ports
ENV     CONTAINER_PORT=5000 \
        BIND_INTERFACE=0.0.0.0 \
        GRACEFUL_TIMEOUT=300 \
        TIMEOUT=300 \
        WORKER_CONNECTIONS=10 \
        WORKERS=3 \
        DATABASE_URL=sqlite:///./default.db \
        LINKA_MASTER_KEY=""

EXPOSE ${CONTAINER_PORT}

# run gunicorn
CMD ["sh", "./startup.sh"]

