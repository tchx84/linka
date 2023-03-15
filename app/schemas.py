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
from enum import Enum
from pydantic import BaseModel, Field, validator
from pydantic.dataclasses import dataclass
from typing import Optional, Union
from fastapi import Query


class Measurement(BaseModel):
    sensor: str = Field(
        ...,
        title="Sensor",
        description="Model of the device",
    )
    source: str = Field(
        ...,
        title="Source",
        description="Name used to identify the device",
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="User friendly name to identify the device",
    )
    version: Optional[str] = Field(
        None,
        title="Version",
        description="Firmware version of the device",
    )
    pm1dot0: Optional[float] = Field(
        None,
        title="PM1.0",
        description="Concentration of PM1.0 inhalable particles per ug/m3",
        ge=0,
        le=500,
    )
    pm2dot5: Optional[float] = Field(
        None,
        title="PM2.5",
        description="Concentration of PM2.5 inhalable particles per ug/m3",
        ge=0,
        le=500,
    )
    pm10: Optional[float] = Field(
        None,
        title="PM10",
        description="Concentration of PM10 inhalable particles per ug/m3",
        ge=0,
        le=500,
    )
    humidity: Optional[float] = Field(
        None,
        title="Humidity",
        description="Concentration of water vapor present in the air",
        ge=1.0,  # Coober Pedy, South Australia
        le=100.0,  # Sea ?
    )
    temperature: Optional[float] = Field(
        None,
        title="Temperature",
        description="Temperature in celsius degrees",
        ge=-89.2,  # Vostok, Antarctica
        le=134.0,  # Death Valley, California
    )
    pressure: Optional[float] = Field(
        None,
        title="Pressure",
        description="Pressure within the atmosphere of Earth in hPa",
        ge=870.0,  # Typhoon Tip, Pacific Ocean
        le=1084.0,  # Agata, Siberia
    )
    co2: Optional[float] = Field(
        None,
        title="CO2",
        description="Carbon dioxide concentration in ppm",
        ge=50.0,  # Closed system with plants
        le=80000.0,  # Twice the IDLH
    )
    longitude: float = Field(
        ...,
        title="Longitud",
        description="Physical longitude coordinate of the device",
        ge=-180,
        le=180,
    )
    latitude: float = Field(
        ...,
        title="Latitude",
        description="Physical latitude coordinate of the device",
        ge=-90,
        le=90,
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

    def to_orm(self, provider):
        _dict = self.dict()
        _dict["provider_id"] = provider
        return _dict

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
        description="Target longitude coordinate",
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


class Provider(BaseModel):
    provider: str = Field(
        ...,
        title="Provider",
        description="Name used to identify the measurements provider",
    )

    class Config:
        orm_mode = True


class APIKey(BaseModel):
    key: str = Field(
        ...,
        title="API key",
        description="The API key needed for authorization",
    )


class Category(str, Enum):
    GOOD = "Good"
    MODERATE = "Moderate"
    UNHEALTHY_FOR_SENSITIVE_GROUPS = "Unhealthy for Sensitive Groups"
    UNHEALTHY = "Unhealthy"
    VERY_UNHEALTHY = "Very Unhealthy"
    HAZARDOUS = "Hazardous"


class Quality(BaseModel):
    category: Category = Field(
        ...,
        title="Category",
        description="Category according to the air quality index",
    )
    index: int = Field(
        ...,
        title="Index",
        description="Index of the air quality",
    )


class Report(BaseModel):
    sensor: str = Field(
        ...,
        title="Sensor",
        description="Model of the device",
    )
    source: str = Field(
        ...,
        title="Source",
        description="Name used to identify the device",
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="User friendly name to identify the device",
    )
    longitude: float = Query(
        None,
        title="Longitude",
        description="Target longitude coordinate",
    )
    latitude: float = Query(
        None,
        title="Latitude",
        description="Target latitude coordinate",
    )
    quality: Quality = Field(
        None,
        title="Quality",
        description="Quality according to AQI",
    )


class BasicStats(BaseModel):
    average: Union[float, None]
    maximum: Union[float, None]
    minimum: Union[float, None]


class ReportStats(BaseModel):
    sensor: str = Field(
        ...,
        title="Sensor",
        description="Model of the device",
    )
    source: str = Field(
        ...,
        title="Source",
        description="Name used to identify the device",
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="User friendly name to identify the device",
    )
    longitude: float = Query(
        None,
        title="Longitude",
        description="Target longitude coordinate",
    )
    latitude: float = Query(
        None,
        title="Latitude",
        description="Target latitude coordinate",
    )
    pm1dot0: BasicStats = Field(
        ..., title="pm1dot0", description="Basic stats from pm1dot0"
    )
    pm2dot5: BasicStats = Field(
        ..., title="pm2dot5", description="Basic stats from pm2dot5"
    )
    pm10: BasicStats = Field(..., title="pm10", description="Basic stats from pm10")
    humidity: BasicStats = Field(
        ..., title="humidity", description="Basic stats from humidity"
    )
    temperature: BasicStats = Field(
        ..., title="temperature", description="Basic stats from temperature"
    )
    pressure: BasicStats = Field(
        ..., title="pressure", description="Basic stats from pressure"
    )
    co2: BasicStats = Field(..., title="CO2", description="Basic stats from CO2")


class Status(str, Enum):
    UP = "UP"
    DOWN = "DOWN"


class ServiceStatus(BaseModel):
    service: Status = Field(
        Status.UP,
        title="Service",
        description="Operational status of the service",
    )
    database: Status = Field(
        Status.UP,
        title="Database",
        description="Operational status of the database",
    )
