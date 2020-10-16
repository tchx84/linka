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

import os
import databases
import sqlalchemy


class Vault(object):

    def __init__(self):
        self._url = os.environ.get('RALD_DB_URL', 'sqlite:///./default.db')
        self._database = databases.Database(self._url)
        self._metadata = sqlalchemy.MetaData()

    def setup(self):
        self._measurements = sqlalchemy.Table(
            'measurements',
            self._metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('recorded', sqlalchemy.DateTime),
            sqlalchemy.Column('sensor', sqlalchemy.String),
            sqlalchemy.Column('source', sqlalchemy.String),
            sqlalchemy.Column('pm1dot0', sqlalchemy.Float),
            sqlalchemy.Column('pm2dot5', sqlalchemy.Float),
            sqlalchemy.Column('pm10', sqlalchemy.Float),
            sqlalchemy.Column('longitude', sqlalchemy.Float),
            sqlalchemy.Column('latitude', sqlalchemy.Float),
        )

        self._engine = sqlalchemy.create_engine(
            self._url, connect_args={"check_same_thread": False}
        )

        self._metadata.create_all(self._engine)

        return self

    async def startup(self):
        await self._database.connect()

    async def shutdown(self):
        await self._database.disconnect()

    async def store(self, measurement):
        insert = self._measurements.insert()
        await self._database.execute(insert, measurement)

    async def retrieve(self, query):
        select = self._measurements.select()

        if query.start is not None:
            select = select.where(self._measurements.c.recorded >= query.start)
        if query.end is not None:
            select = select.where(self._measurements.c.recorded <= query.end)
        if query.source is not None:
            select = select.where(self._measurements.c.source == query.source)

        return await self._database.fetch_all(select)
