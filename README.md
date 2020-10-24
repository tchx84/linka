# rald-server

Red de Aire Libre Descentralizada

## Install

```
$ sudo dnf install python3-virtualenv
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

## Setup

```
$ export DATABASE_URL=sqlite:///./default.db
$ alembic upgrade head
$ ./rald-cli api-keys create app
Your new API key is: f710b83cee5f43d2b73cbec810dc842c (use the new generated API key)
```

## Run

```
$ gunicorn --bind 0.0.0.0:5000 --graceful-timeout 300 --timeout 300 --worker-class=uvicorn.workers.UvicornWorker --worker-connections=10 --workers=3 wsgi-service:app
```

## Docker

```
# docker build -t rald-server .
# docker run -d -p 5000:5000 --name rald-server rald-server
```

When running, you can set the following environment variables:

| Variable           | Default Value               |
|--------------------|-----------------------------|
| CONTAINER_PORT     | 5000                        |
| BIND_INTERFACE     | 0.0.0.0                     |
| GRACEFUL_TIMEOUT   | 300                         |
| TIMEOUT            | 300                         |
| WORKER_CONNECTIONS | 10                          |
| WORKERS            | 3                           |
| DATABASE_URL       | sqlite:///./default.db      |

## Docs

Check http://localhost:5000/docs
