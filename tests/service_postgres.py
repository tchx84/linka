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

import os
import sys

# import asyncio
# from app import models
# from app.db import db

import copy
import pytest

from urllib.parse import urlencode
from alembic import config
from fastapi.testclient import TestClient


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# client = None
test_db_path = "test.db"
headers = {"X-API-Key": ""}
measurements = [
    {
        "sensor": "test",
        "source": "test",
        "description": None,
        "version": None,
        "pm1dot0": 0.0,
        "pm2dot5": 0.0,
        "pm10": 0.0,
        "humidity": 1.0,
        "temperature": -89.2,
        "pressure": 870.0,
        "co2": 200.0,
        "longitude": -57.521369,
        "latitude": -25.194156,
        "recorded": "2020-10-24T20:47:57.370721+00:00",
    },
    {
        "sensor": "aqi",
        "source": "aqi",
        "description": "aqi",
        "version": None,
        "pm1dot0": 26.4,
        "pm2dot5": 26.4,
        "pm10": 26.4,
        "humidity": 100.0,
        "temperature": 134.0,
        "pressure": 1084.0,
        "co2": 1000.0,
        "longitude": -57.521369,
        "latitude": -25.194156,
        "recorded": "2020-10-24T20:47:57.370721+00:00",
    },
    {
        "sensor": "nullable",
        "source": "nullable",
        "description": "nullable",
        "version": "nullable",
        "pm1dot0": None,
        "pm2dot5": None,
        "pm10": None,
        "humidity": None,
        "temperature": None,
        "pressure": None,
        "co2": None,
        "longitude": -57.521369,
        "latitude": -25.194156,
        "recorded": "2020-10-24T20:47:57.370721+00:00",
    },
]
aqi = [
    {
        "source": "aqi",
        "sensor": "aqi",
        "description": "aqi",
        "longitude": -57.521369,
        "latitude": -25.194156,
        "quality": {"category": "Moderate", "index": 81},
    },
    {
        "source": "nullable",
        "sensor": "nullable",
        "description": "nullable",
        "longitude": -57.521369,
        "latitude": -25.194156,
        "quality": None,
    },
    {
        "source": "test",
        "sensor": "test",
        "description": None,
        "longitude": -57.521369,
        "latitude": -25.194156,
        "quality": {"category": "Good", "index": 0},
    },
]
stats = [
    {
        "source": "aqi",
        "sensor": "aqi",
        "description": "aqi",
        "longitude": -57.521369,
        "latitude": -25.194156,
        "pm10": {"average": 26.4, "maximum": 26.4, "minimum": 26.4},
        "pm1dot0": {"average": 26.4, "maximum": 26.4, "minimum": 26.4},
        "pm2dot5": {"average": 26.4, "maximum": 26.4, "minimum": 26.4},
        "humidity": {"average": 100.0, "maximum": 100.0, "minimum": 100.0},
        "pressure": {"average": 1084.0, "maximum": 1084.0, "minimum": 1084.0},
        "co2": {"average": 1000.0, "maximum": 1000.0, "minimum": 1000.0},
        "temperature": {"average": 134.0, "maximum": 134.0, "minimum": 134.0},
    },
    {
        "sensor": "nullable",
        "source": "nullable",
        "description": "nullable",
        "longitude": -57.521369,
        "latitude": -25.194156,
        "pm10": {"average": None, "maximum": None, "minimum": None},
        "pm1dot0": {"average": None, "maximum": None, "minimum": None},
        "pm2dot5": {"average": None, "maximum": None, "minimum": None},
        "humidity": {"average": None, "maximum": None, "minimum": None},
        "pressure": {"average": None, "maximum": None, "minimum": None},
        "co2": {"average": None, "maximum": None, "minimum": None},
        "temperature": {"average": None, "maximum": None, "minimum": None},
    },
    {
        "sensor": "test",
        "source": "test",
        "description": None,
        "longitude": -57.521369,
        "latitude": -25.194156,
        "pm10": {"average": 0.0, "maximum": 0.0, "minimum": 0.0},
        "pm1dot0": {"average": 0.0, "maximum": 0.0, "minimum": 0.0},
        "pm2dot5": {"average": 0.0, "maximum": 0.0, "minimum": 0.0},
        "humidity": {"average": 1.0, "maximum": 1.0, "minimum": 1.0},
        "pressure": {"average": 870.0, "maximum": 870.0, "minimum": 870.0},
        "co2": {"average": 200.0, "maximum": 200.0, "minimum": 200.0},
        "temperature": {"average": -89.2, "maximum": -89.2, "minimum": -89.2},
    },
]
status = {
    "service": "UP",
    "database": "UP",
}

MASTER_KEY = "EaDEFOuNiscENyok"
master_headers = {"X-API-Key": MASTER_KEY}
provider = {"provider": "test"}


@pytest.fixture()
def client():
    from app import service

    # from app import db
    # from app import models
    # import asyncio

    with TestClient(service.app) as client:
        yield client
        # headers["X-API-Key"] = asyncio.run(models.Provider.create_new_key(db, "test"))


def setup_module(client):

    os.environ["LINKA_MASTER_KEY"] = MASTER_KEY
    config.main(argv=["upgrade", "head"])
    # headers["X-API-Key"] = asyncio.run(models.Provider.create_new_key(db, "test"))


# async def teardown_module():
# await db.disconnect()


def test_record(client):
    response = client.post("/api/v1/measurements", json=measurements, headers=headers)
    assert response.status_code == 200


def test_invalid_api_key_access(client):
    response = client.post(
        "/api/v1/measurements", json=measurements, headers={"X-API-Key": "123"}
    )
    assert response.status_code == 403


def test_query(client):
    query = {
        "start": "1984-04-24T00:00:00",
    }

    response = client.get(f"/api/v1/measurements?{urlencode(query)}")
    assert response.status_code == 200
    assert response.json() == measurements


def test_empty_query(client):
    query = {
        "source": "test",
        "start": "1984-04-24T00:00:00",
        "end": "1984-04-25T00:00:00",
    }

    response = client.get(f"/api/v1/measurements?{urlencode(query)}")
    assert response.status_code == 200
    assert response.json() == []


def test_distance_query(client):
    query = {
        "start": "1984-04-24T00:00:00",
        "longitude": -57.521369,
        "latitude": -25.194156,
        "distance": "100",
    }

    response = client.get(f"/api/v1/measurements?{urlencode(query)}")
    assert response.status_code == 200
    assert response.json() == measurements


def test_enforce_utc():
    original = measurements[0]

    future = copy.deepcopy(original)
    future["recorded"] = "2020-10-24T21:47:57.370721+01:00"

    present = copy.deepcopy(original)
    present["recorded"] = "2020-10-24T20:47:57.370721"

    past = copy.deepcopy(original)
    past["recorded"] = "2020-10-24T19:47:57.370721-01:00"

    from app.schemas import Measurement

    original = Measurement(**original)
    future = Measurement(**future)
    present = Measurement(**present)
    past = Measurement(**past)

    assert original == future
    assert original == present
    assert original == past


def test_create_provider(client):
    response = client.post("/api/v1/providers", json=provider, headers=master_headers)

    assert response.status_code == 200


def test_list_providers(client):
    response = client.get("/api/v1/providers", headers=master_headers)

    assert response.status_code == 200
    assert response.json() == [provider]


def test_delete_provider(client):
    response = client.delete("/api/v1/providers/test", headers=master_headers)

    assert response.status_code == 200

    response = client.get("/api/v1/providers", headers=master_headers)

    assert response.status_code == 200
    assert response.json() == []


def test_aqi(client):
    query = {
        "start": "1984-04-24T00:00:00",
    }

    response = client.get(f"/api/v1/aqi?{urlencode(query)}")
    assert response.status_code == 200
    assert response.json() == aqi


def test_stats(client):
    query = {"start": "1984-04-24T00:00:00"}

    response = client.get(f"/api/v1/stats?{urlencode(query)}")
    assert response.status_code == 200
    assert response.json() == stats


def test_status(client):
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json() == status
