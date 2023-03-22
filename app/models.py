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
from typing import Dict, List, Set, Tuple, Union

from .db import metadata


measurements = sqlalchemy.Table(
    "measurements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("recorded", sqlalchemy.DateTime(timezone=True)),
    sqlalchemy.Column("sensor", sqlalchemy.String),
    sqlalchemy.Column("source", sqlalchemy.String),
    sqlalchemy.Column("version", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("pm1dot0", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("pm2dot5", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("pm10", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("humidity", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("temperature", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("pressure", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("co2", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column(
        "provider_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("providers.id", ondelete="CASCADE"),
        nullable=True,
    ),
)

providers = sqlalchemy.Table(
    "providers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("provider", sqlalchemy.String, nullable=False),
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
        measurements_dict = {
            "pm1dot0": measurements.c.pm1dot0,
            "pm2dot5": measurements.c.pm2dot5,
            "pm10": measurements.c.pm10,
            "humidity": measurements.c.humidity,
            "temperature": measurements.c.temperature,
            "pressure": measurements.c.pressure,
            "co2": measurements.c.co2,
        }
        measurements_stats = [
            measurements.c.sensor,
            measurements.c.source,
            measurements.c.description,
            measurements.c.latitude,
            measurements.c.longitude,
        ]
        for measurement in measurements_dict.keys():
            measurements_stats.extend(
                [
                    func.avg(measurements_dict[measurement]).label(
                        f"{measurement}_average"
                    ),
                    func.max(measurements_dict[measurement]).label(
                        f"{measurement}_maximum"
                    ),
                    func.min(measurements_dict[measurement]).label(
                        f"{measurement}_minimum"
                    ),
                ]
            )

        select = sqlalchemy.select(measurements_stats)
        select = select.group_by(
            measurements.c.sensor,
            measurements.c.source,
            measurements.c.description,
            measurements.c.latitude,
            measurements.c.longitude,
        )
        select = select.order_by(sqlalchemy.asc(measurements.c.description))
        select = Measurement.filter(select, query)

        return await db.fetch_all(select)

    @staticmethod
    async def retrieve(db, query):
        select = measurements.select()
        select = select.order_by(sqlalchemy.asc(measurements.c.description))
        select = Measurement.filter(select, query)

        return await db.fetch_all(select)


class Provider:
    @staticmethod
    async def store(db: Database, api_key: Dict) -> None:
        insert = providers.insert()
        await db.execute(insert, api_key)

    @staticmethod
    async def create_new_key(db: Database, provider: str) -> str:
        raw_api_key = uuid.uuid4().hex
        api_key_hash = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
        api_key = {"provider": provider, "api_key_hash": api_key_hash}
        await Provider.store(db, api_key)
        return raw_api_key

    @staticmethod
    async def get_providers(db: Database) -> List[Tuple[str, int]]:
        query = sqlalchemy.select(
            [providers.c.provider, sqlalchemy.func.count(providers.c.provider)]
        ).group_by(providers.c.provider)
        query = query.order_by(sqlalchemy.asc(providers.c.provider))
        return await db.fetch_all(query)

    @staticmethod
    async def revoke_key(db: Database, provider: str, raw_api_key: str) -> bool:
        api_key_hash = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
        delete = providers.delete()
        query = delete.where(providers.c.provider == provider)
        query = query.where(providers.c.api_key_hash == api_key_hash)
        return await db.execute(query)

    @staticmethod
    async def revoke_all_keys(db: Database, provider: str) -> bool:
        delete = providers.delete()
        query = delete.where(providers.c.provider == provider)
        return await db.execute(query)

    @staticmethod
    async def get_all_keys(db: Database) -> Set[str]:
        query = sqlalchemy.select([providers.c.api_key_hash])
        query = query.order_by(sqlalchemy.asc(providers.c.provider))
        keys = await db.fetch_all(query)
        return {k[0] for k in keys}

    @staticmethod
    async def get_provider_for_key(db: Database, api_key_hash: str) -> Union[str, None]:
        query = sqlalchemy.select([providers.c.id, providers.c.api_key_hash])
        query = query.where(providers.c.api_key_hash == api_key_hash)
        provider = await db.fetch_one(query)
        return provider[0] if provider else None
