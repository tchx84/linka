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
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import List


from .models import Measurement, Query, QueryResult

from .authentication import get_current_username

app = FastAPI()





@app.post('/api/v1/record')
async def record(measurements: List[Measurement], username: str = Depends(get_current_username)):
    pass


@app.get('/api/v1/query')
async def query(query: Query, username: str = Depends(get_current_username)):
    return QueryResult()
