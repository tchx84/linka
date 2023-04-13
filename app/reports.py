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
        report = schemas.Report(
            sensor=source.sensor,
            source=source.source,
            description=source.description,
            latitude=source.latitude,
            longitude=source.longitude,
            quality=None,
        )

        if source.pm2dot5_average is None:
            return report

        concentration = next(
            (c for c in CONCENTRATIONS if source.pm2dot5_average <= c[1]),
            CONCENTRATIONS[-1],
        )

        breakpoint_index = CONCENTRATIONS.index(concentration)
        breakpoint = BREAKPOINTS[breakpoint_index]

        index = (
            (breakpoint[1] - breakpoint[0]) / (concentration[1] - concentration[0])
        ) * (source.pm2dot5_average - concentration[0]) + breakpoint[0]
        index_breakpoint = next(
            (b for b in BREAKPOINTS if index <= b[1]),
            BREAKPOINTS[-1],
        )

        category_index = BREAKPOINTS.index(index_breakpoint)
        category = CATEGORIES[category_index]

        report.quality = schemas.Quality(index=index, category=category)

        return report

    @staticmethod
    async def generate(db, query):
        sources = await Measurement.stats(db, query)
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
            pm1dot0=schemas.BasicStats(
                average=source.pm1dot0_average,
                maximum=source.pm1dot0_maximum,
                minimum=source.pm1dot0_minimum,
            ),
            pm2dot5=schemas.BasicStats(
                average=source.pm2dot5_average,
                maximum=source.pm2dot5_maximum,
                minimum=source.pm2dot5_minimum,
            ),
            pm10=schemas.BasicStats(
                average=source.pm10_average,
                maximum=source.pm10_maximum,
                minimum=source.pm10_minimum,
            ),
            humidity=schemas.BasicStats(
                average=source.humidity_average,
                maximum=source.humidity_maximum,
                minimum=source.humidity_minimum,
            ),
            temperature=schemas.BasicStats(
                average=source.temperature_average,
                maximum=source.temperature_maximum,
                minimum=source.temperature_minimum,
            ),
            pressure=schemas.BasicStats(
                average=source.pressure_average,
                maximum=source.pressure_maximum,
                minimum=source.pressure_minimum,
            ),
            co2=schemas.BasicStats(
                average=source.co2_average,
                maximum=source.co2_maximum,
                minimum=source.co2_minimum,
            ),
        )

    @staticmethod
    async def generate(db, query):
        sources = await Measurement.stats(db, query)
        return [Stats.get_stat(s) for s in sources]
