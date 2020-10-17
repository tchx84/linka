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

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from typing import Optional
from fastapi import Query


class Measurement(BaseModel):

    sensor: str
    source: str
    pm1dot0: Optional[float] = None
    pm2dot5: Optional[float] = None
    pm10: Optional[float] = None
    longitude: float
    latitude: float
    recorded: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        orm_mode = True


@dataclass
class QueryParams:

    source: str = Query(None)
    start: datetime = Query(None)
    end: datetime = Query(None)
