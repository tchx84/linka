# LINKA

LINKA is an open source backend service to record air quality data from sensors.

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
$ ./rald-cli api-keys create linka
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

## API Keys Management
Create, list and revoke the API keys for a specific source.

### create
`$ rald-cli api-keys create SOURCE`

### list
`$ rald-cli api-keys list`

### revoke
`$ rald-cli api-keys revoke SOURCE [--all] [--key]`

Either provide `--all` for revoking all the keys associated to a source or `--key` to revoke a single key.

## Docs

Check http://localhost:5000/docs

# Disclaimer

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
