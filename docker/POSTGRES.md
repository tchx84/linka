# Migrate from SQLite to PostgreSQL

## Stop the container

```
$ docker stop linka
```

## Make a copy of your current SQLite database

```
$ cp /path/to/default.db /path/to/backup.db
```

## Install PostgreSQL and create the database

```
$ docker pull postgres
$ docker run -itd -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=<PASSWORD> -p 5432:5432 -v /path/to/postgres/data:/var/lib/postgresql/data --name postgres postgres
$ PGPASSWORD=<PASSWORD> psql -U postgres --host localhost
$ CREATE DATABASE linka;
$ \q
```

## Clone linka project and setup the database

```
$ git clone https://github.com/tchx84/linka.git
$ cd linka
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt

# Make sure both are on the same version

$ export DATABASE_URL=sqlite:///path/to/backup.db
$ alembic upgrade head

$ export DATABASE_URL=postgresql://postgres:<PASSWORD>@localhost:5432/linka
$ alembic upgrade head

# XXX A necessary hack
$ PGPASSWORD=<PASSWORD> psql -U postgres --host localhost
$ \c linka
$ DELETE FROM alembic_version;
```

## Install pgloader and migrate the database

```
$ docker pull ghcr.io/dimitri/pgloader:latest
$ docker run --rm -it ghcr.io/dimitri/pgloader:latest pgloader --version
```

Save the command from above to a file called "db.load".

```
load database from sqlite:///host/path/to/backup.db into postgresql://postgres:<PASSWORD>@localhost:5432/linka with create no tables;
```

And run it

```
$ docker run -ti --privileged --net=host --pid=host --ipc=host --volume /:/host ghcr.io/dimitri/pgloader:latest pgloader /host/path/to/db.load
```

**NOTE** that the /host prefix is mandatory due to how we're mounting the host volume.
