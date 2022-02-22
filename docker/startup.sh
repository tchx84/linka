#!/bin/bash
# rald-server startup script

check_env_variable() {
  if [ -z $1 ]; then
    echo "$2 environment variable not set";
    exit 1
  fi
  echo "$2 -> $1"
}

echo "staring up rald-server..."

echo "Checking environment variales:"
check_env_variable $BIND_INTERFACE "BIND_INTERFACE"
check_env_variable $CONTAINER_PORT "CONTAINER_PORT"
check_env_variable $GRACEFUL_TIMEOUT "GRACEFUL_TIMEOUT"
check_env_variable $TIMEOUT "TIMEOUT"
check_env_variable $WORKER_CONNECTIONS "WORKER_CONNECTIONS"
check_env_variable $WORKERS "WORKERS"

cd /app
alembic upgrade head
gunicorn --bind ${BIND_INTERFACE}:${CONTAINER_PORT} --graceful-timeout ${GRACEFUL_TIMEOUT} --timeout ${TIMEOUT} --worker-class=uvicorn.workers.UvicornWorker --worker-connections ${WORKER_CONNECTIONS} --workers ${WORKERS} wsgi-service:app
