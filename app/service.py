# Copyright 2020 Martín Abente Lahaye
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
from . import reports
from .db import db
from .authentication import validate_api_key, validate_master_key


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.post("/api/v1/sources", response_model=schemas.APIKey)
async def create_source(
    source: schemas.Source, key: APIKey = Depends(validate_master_key)
):
    key = await models.APIKey.create_new_key(db, source.source)
    return schemas.APIKey(key=key)


@app.get("/api/v1/sources")
async def list_sources(key: APIKey = Depends(validate_master_key)):
    return [schemas.Source.from_orm(s) for s in await models.APIKey.get_sources(db)]


@app.delete("/api/v1/sources/{source}")
async def delete_source(source: str, key: APIKey = Depends(validate_master_key)):
    return await models.APIKey.revoke_all_keys(db, source)


@app.post("/api/v1/measurements")
async def post(
    measurements: List[schemas.Measurement], key: APIKey = Depends(validate_api_key)
):
    await models.Measurement.store(db, [m.dict() for m in measurements])


@app.get("/api/v1/measurements", response_model=List[schemas.Measurement])
async def get(query: schemas.QueryParams = Depends(schemas.QueryParams)):
    return [
        schemas.Measurement.from_orm(m)
        for m in await models.Measurement.retrieve(db, query)
    ]


@app.get("/api/v1/aqi", response_model=List[schemas.Report])
async def aqi(query: schemas.QueryParams = Depends(schemas.QueryParams)):
    return await reports.AQI.generate(db, query)


@app.get("/api/v1/stats", response_model=List[schemas.ReportStats])
async def stats(query: schemas.QueryParams = Depends(schemas.QueryParams)):
    return await reports.Stats.generate(db, query)


@app.get("/api/v1/status", response_model=schemas.ServiceStatus)
async def status():
    status = schemas.ServiceStatus()

    if db.connection() is None:
        status.database = schemas.Status.DOWN

    return status
