# Docker

```
$ docker build -t linka docker/
$ docker run -d -p 5000:5000 --name linka linka
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
| LINKA_MASTER_KEY   | ""                          |
