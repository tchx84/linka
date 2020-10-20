# Copyright 2020 Linka González
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

from .db import metadata


measurements = sqlalchemy.Table(
    'measurements',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('recorded', sqlalchemy.DateTime),
    sqlalchemy.Column('sensor', sqlalchemy.String),
    sqlalchemy.Column('source', sqlalchemy.String),
    sqlalchemy.Column('pm1dot0', sqlalchemy.Float, nullable=True),
    sqlalchemy.Column('pm2dot5', sqlalchemy.Float, nullable=True),
    sqlalchemy.Column('pm10', sqlalchemy.Float, nullable=True),
    sqlalchemy.Column('longitude', sqlalchemy.Float),
    sqlalchemy.Column('latitude', sqlalchemy.Float),
)


class Measurement:

    @staticmethod
    async def store(db, measurements_):
        insert = measurements.insert()
        await db.execute_many(insert, measurements_)

    @staticmethod
    async def retrieve(db, query):
        select = measurements.select()

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

        return await db.fetch_all(select)
