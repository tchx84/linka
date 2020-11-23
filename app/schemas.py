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

from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field, validator
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
    recorded: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator("recorded")
    def must_be_utc(cls, v):
        v = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        v = datetime.utcfromtimestamp(v.timestamp())
        v = v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        orm_mode = True


@dataclass
class QueryParams:

    source: str = Query(None)
    start: datetime = Query(None)
    end: datetime = Query(None)
    longitude: float = Query(None)
    latitude: float = Query(None)
    distance: float = Query(None)

    @validator("start")
    def only_recent(cls, v):
        v = v if v else datetime.now(timezone.utc) - timedelta(minutes=5)
        return v


class Source(BaseModel):

    source: str

    class Config:
        orm_mode = True


class APIKey(BaseModel):

    key: str
