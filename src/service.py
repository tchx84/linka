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
from typing import List

from .vault import Vault
from .models import Measurement, QueryParams

app = FastAPI()
vault = Vault().setup()


@app.on_event("startup")
async def startup():
    await vault.startup()


@app.on_event("shutdown")
async def shutdown():
    await vault.shutdown()


@app.post('/api/v1/record')
async def record(measurement: Measurement):
    await vault.store(measurement.dict())


@app.get('/api/v1/query', response_model=List[Measurement])
async def query(query: QueryParams = Depends(QueryParams)):
    return [Measurement.from_orm(m) for m in await vault.retrieve(query)]
