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

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Measurement(BaseModel):

    temperature: float
    humidity: float
    light: float
    noise: float
    quality: float


class Query(BaseModel):

    start: Optional[datetime] = None
    end: Optional[datetime] = None


class QueryResult(BaseModel):

    measurements: List[Measurement] = []
