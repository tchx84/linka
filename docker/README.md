# Docker

Run from source cloned directory

```
$ docker build -t linka -f docker/Dockerfile .
$ docker run -d -p 5000:5000 -e LINKA_MASTER_KEY="YOUR_MADE_UP_AND_SECURE_API_KEY" --name linka linka
```

When running, you can set the following environment variables through `-e` command line switch (one for each variable) or within a file using `--env-file $YOUR_ENV_FILE` :

| Variable           | Default Value                     |
| ------------------ | --------------------------------- |
| CONTAINER_PORT     | 5000                              |
| BIND_INTERFACE     | 0.0.0.0                           |
| GRACEFUL_TIMEOUT   | 300                               |
| TIMEOUT            | 300                               |
| WORKER_CONNECTIONS | 10                                |
| WORKERS            | 3                                 |
| DATABASE_URL       | sqlite:///./default.db            |
| LINKA_MASTER_KEY   | "YOUR_MADE_UP_AND_SECURE_API_KEY" |

This are development instructions. 

--- 

For a production or persistent environment you should setup a custom `IMAGE_NAME`, PostgreSQL database, remote access, etc.

Example:

`docker run -d --env-file $ENV_FILE -p 5858:5000 -p 5822:22 --name linka-server $IMAGE_NAME`



`ENV_FILE`

```
DATABASE_URL=postgresql://<USER>:<PASSWORD>@<ADDRESS>:5432/linka
LINKA_MASTER_KEY=ALGUN_MASTER_KEY
```

If you're currently using SQLite, and want to migrate to PostgreSQL, check [this](POSTGRES.md) guide.
