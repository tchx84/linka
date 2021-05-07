# Copyright 2020 Martín Abente Lahaye
# Copyright 2020 Samuel Cantero
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import geopy
import geopy.distance
import sqlalchemy
import uuid
import hashlib

from sqlalchemy import func
from databases.core import Database
from typing import Dict, List, Set, Tuple

from .db import metadata


measurements = sqlalchemy.Table(
    "measurements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("recorded", sqlalchemy.DateTime),
    sqlalchemy.Column("sensor", sqlalchemy.String),
    sqlalchemy.Column("source", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("pm1dot0", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("pm2dot5", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("pm10", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("humidity", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("temperature", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("pressure", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
)

api_keys = sqlalchemy.Table(
    "api_keys",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("source", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("api_key_hash", sqlalchemy.String(length=65), nullable=False),
)


class Measurement:
    @staticmethod
    async def store(db, measurements_):
        insert = measurements.insert()
        await db.execute_many(insert, measurements_)

    @staticmethod
    def filter(select, query):
        if query.start is not None:
            select = select.where(measurements.c.recorded >= query.start)
        if query.end is not None:
            select = select.where(measurements.c.recorded <= query.end)
        if query.source is not None:
            select = select.where(measurements.c.source == query.source)
        if query.distance is not None:
            longitude = query.longitude if query.longitude is not None else 0.0
            latitude = query.latitude if query.latitude is not None else 0.0
            location = geopy.Point(latitude, longitude)
            distance = geopy.distance.distance(kilometers=query.distance)

            north = distance.destination(point=location, bearing=0)
            east = distance.destination(point=location, bearing=90)
            south = distance.destination(point=location, bearing=180)
            west = distance.destination(point=location, bearing=270)

            select = select.where(measurements.c.latitude <= north.latitude)
            select = select.where(measurements.c.longitude <= east.longitude)
            select = select.where(measurements.c.latitude >= south.latitude)
            select = select.where(measurements.c.longitude >= west.longitude)

        return select

    @staticmethod
    async def stats(db, query):
        select = sqlalchemy.select(
            [
                measurements.c.sensor,
                measurements.c.source,
                measurements.c.description,
                measurements.c.latitude,
                measurements.c.longitude,
                func.avg(measurements.c.pm2dot5).label("average"),
                func.max(measurements.c.pm2dot5).label("maximum"),
                func.min(measurements.c.pm2dot5).label("minimum"),
            ]
        )
        select = select.group_by(
            measurements.c.sensor,
            measurements.c.source,
            measurements.c.description,
            measurements.c.latitude,
            measurements.c.longitude,
        )
        select = Measurement.filter(select, query)

        return await db.fetch_all(select)

    @staticmethod
    async def retrieve(db, query):
        select = measurements.select()
        select = Measurement.filter(select, query)

        return await db.fetch_all(select)


class APIKey:
    @staticmethod
    async def store(db: Database, api_key: Dict) -> None:
        insert = api_keys.insert()
        await db.execute(insert, api_key)

    @staticmethod
    async def create_new_key(db: Database, source: str) -> str:
        raw_api_key = uuid.uuid4().hex
        api_key_hash = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
        api_key = {"source": source, "api_key_hash": api_key_hash}
        await APIKey.store(db, api_key)
        return raw_api_key

    @staticmethod
    async def get_sources(db: Database) -> List[Tuple[str, int]]:
        query = sqlalchemy.select(
            [api_keys.c.source, sqlalchemy.func.count(api_keys.c.source)]
        ).group_by(api_keys.c.source)
        return await db.fetch_all(query)

    @staticmethod
    async def revoke_key(db: Database, source: str, raw_api_key: str) -> bool:
        api_key_hash = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
        delete = api_keys.delete()
        query = delete.where(api_keys.c.source == source)
        query = query.where(api_keys.c.api_key_hash == api_key_hash)
        return await db.execute(query)

    @staticmethod
    async def revoke_all_keys(db: Database, source: str) -> bool:
        delete = api_keys.delete()
        query = delete.where(api_keys.c.source == source)
        return await db.execute(query)

    @staticmethod
    async def get_all_keys(db: Database) -> Set[str]:
        query = sqlalchemy.select([api_keys.c.api_key_hash])
        keys = await db.fetch_all(query)
        return {k[0] for k in keys}
