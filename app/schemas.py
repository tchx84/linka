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

    sensor: str = Field(
        ...,
        title="Sensor",
        description="Model of the sensor device",
    )
    source: str = Field(
        ...,
        title="Source",
        description="Name used to identify the device",
    )
    pm1dot0: Optional[float] = Field(
        None,
        title="PM1.0",
        description="Concentration of PM1.0 inhalable particles per ug/m3",
    )
    pm2dot5: Optional[float] = Field(
        None,
        title="PM2.5",
        description="Concentration of PM2.5 inhalable particles per ug/m3",
    )
    pm10: Optional[float] = Field(
        None,
        title="PM10",
        description="Concentration of PM10 inhalable particles per ug/m3",
    )
    longitude: float = Field(
        ...,
        title="Longitud",
        description="Physical longitud coordinate of the device",
    )
    latitude: float = Field(
        ...,
        title="Latitude",
        description="Physical latitude coordinate of the device",
    )
    recorded: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Recorded",
        description="Date and time for when these values were measured",
    )

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

    source: str = Query(
        None,
        title="Source",
        description="Include measurements from this source only",
    )
    start: datetime = Query(
        None,
        title="Start",
        description="Include measurements after this date and time",
    )
    end: datetime = Query(
        None,
        title="End",
        description="Include measurements before this date and time",
    )
    longitude: float = Query(
        None,
        title="Longitude",
        description="Target longitud coordinate",
    )
    latitude: float = Query(
        None,
        title="Latitude",
        description="Target latitude coordinate",
    )
    distance: float = Query(
        None,
        title="Distance",
        description="Include measurements that are this kilometers far from the target",
    )

    @validator("start")
    def only_recent(cls, v):
        v = v if v else datetime.now(timezone.utc) - timedelta(minutes=5)
        return v


class Source(BaseModel):

    source: str = Field(
        ...,
        title="Source",
        description="Name used to identify the device",
    )

    class Config:
        orm_mode = True


class APIKey(BaseModel):

    key: str = Field(
        ...,
        title="API key",
        description="The API key needed for authorization",
    )
