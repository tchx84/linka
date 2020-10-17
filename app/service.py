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

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKey
from typing import List

from . import models
from . import schemas
from .db import db
from .authentication import get_current_key


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.post('/api/v1/record')
async def record(measurement: schemas.Measurement,
                 key: APIKey = Depends(get_current_key)):
    await models.Measurement.store(db, measurement.dict())


@app.get('/api/v1/query', response_model=List[schemas.Measurement])
async def query(query: schemas.QueryParams = Depends(schemas.QueryParams)):
    return [
        schemas.Measurement.from_orm(m)
        for m in await models.Measurement.retrieve(db, query)
    ]
