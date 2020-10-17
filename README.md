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
$ export SOURCES_PATH=./data/sources.json.example
$ export DATABASE_URL=sqlite:///./default.db
$ alembic upgrade head
```

## Run

```
$ gunicorn --bind 0.0.0.0:5000 --graceful-timeout 300 --timeout 300 --worker-class=uvicorn.workers.UvicornWorker --worker-connections=10 --workers=3 wsgi-service:app
```

## Docs

Check http://localhost:5000/docs
