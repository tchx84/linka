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

from . import schemas
from .models import Measurement


CONCENTRATIONS = [
    [0.0, 12.0],
    [12.1, 35.4],
    [35.5, 55.4],
    [55.5, 150.4],
    [150.5, 250.4],
    [250.5, 350.4],
    [350.5, 500.4],
]

BREAKPOINTS = [
    [0, 50],
    [51, 100],
    [101, 150],
    [151, 200],
    [201, 300],
    [301, 400],
    [401, 500],
]

CATEGORIES = [
    schemas.Category.GOOD,
    schemas.Category.MODERATE,
    schemas.Category.UNHEALTHY_FOR_SENSITIVE_GROUPS,
    schemas.Category.UNHEALTHY,
    schemas.Category.VERY_UNHEALTHY,
    schemas.Category.HAZARDOUS,
    schemas.Category.HAZARDOUS,
]


class AQI:
    @staticmethod
    def get_quality(source):
        concentration = next(
            c for c in CONCENTRATIONS if c[0] <= source.average <= c[1]
        )

        breakpoint_index = CONCENTRATIONS.index(concentration)
        breakpoint = BREAKPOINTS[breakpoint_index]

        index = (
            (breakpoint[1] - breakpoint[0]) / (concentration[1] - concentration[0])
        ) * (source.average - concentration[0]) + breakpoint[0]
        index_breakpoint = next(b for b in BREAKPOINTS if b[0] <= index <= b[1])

        category_index = BREAKPOINTS.index(index_breakpoint)
        category = CATEGORIES[category_index]

        quality = schemas.Quality(index=index, category=category)
        return schemas.Report(
            sensor=source.sensor,
            source=source.source,
            description=source.description,
            latitude=source.latitude,
            longitude=source.longitude,
            quality=quality,
        )

    @staticmethod
    async def generate(db, query):
        sources = await Measurement.average(db, query)
        return [AQI.get_quality(s) for s in sources]


class Stats:
    @staticmethod
    def get_stat(source):
        return schemas.ReportStats(
            sensor=source.sensor,
            source=source.source,
            description=source.description,
            latitude=source.latitude,
            longitude=source.longitude,
            average=source.average,
            maximum=source.maximum,
            minimum=source.minimum,
        )

    @staticmethod
    async def generate(db, query):
        sources = await Measurement.average(db, query)
        return [Stats.get_stat(s) for s in sources]
