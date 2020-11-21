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
import asyncio
import copy

from urllib.parse import urlencode
from alembic import config
from fastapi.testclient import TestClient


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

client = None
test_db_path = 'test.db'
headers = {'X-API-Key': ''}
measurements = [
    {
        'sensor': 'test',
        'source': 'test',
        'pm1dot0': 0.0,
        'pm2dot5': 0.0,
        'pm10': 0.0,
        'longitude': -57.521369,
        'latitude': -25.194156,
        'recorded': '2020-10-24T20:47:57.370721+00:00',
    },
]


def setup_module():
    global client

    if os.path.exists(test_db_path):
        os.unlink(test_db_path)

    os.environ['LINKA_MASTER_KEY'] = 'EaDEFOuNiscENyok'
    os.environ['DATABASE_URL'] = f'sqlite:///./{test_db_path}'
    config.main(argv=['upgrade', 'head'])

    from app.db import db
    from app import models
    headers['X-API-Key'] = asyncio.run(
        models.APIKey.create_new_key(db, 'test')
    )
    from app import service
    client = TestClient(service.app)


def teardown_module():
    if os.path.exists(test_db_path):
        os.unlink(test_db_path)


def test_record():
    response = client.post(
        '/api/v1/measurements', json=measurements, headers=headers
    )
    assert response.status_code == 200


def test_invalid_api_key_access():
    response = client.post(
        '/api/v1/measurements', json=measurements, headers={'X-API-Key': '123'}
    )
    assert response.status_code == 403


def test_query():
    query = {
        'start': '1984-04-24T00:00:00',
    }

    response = client.get(f'/api/v1/measurements?{urlencode(query)}')
    assert response.status_code == 200
    assert response.json() == measurements


def test_empty_query():
    query = {
        'source': 'test',
        'start': '1984-04-24T00:00:00',
        'end': '1984-04-25T00:00:00',
    }

    response = client.get(f'/api/v1/measurements?{urlencode(query)}')
    assert response.status_code == 200
    assert response.json() == []


def test_distance_query():
    query = {
        'start': '1984-04-24T00:00:00',
        'longitude': -57.521369,
        'latitude': -25.194156,
        'distance': '100',
    }

    response = client.get(f'/api/v1/measurements?{urlencode(query)}')
    assert response.status_code == 200
    assert response.json() == measurements


def test_enforce_utc():
    original = measurements[0]

    future = copy.deepcopy(original)
    future['recorded'] = '2020-10-24T21:47:57.370721+01:00'

    present = copy.deepcopy(original)
    present['recorded'] = '2020-10-24T20:47:57.370721'

    past = copy.deepcopy(original)
    past['recorded'] = '2020-10-24T19:47:57.370721-01:00'

    from app.schemas import Measurement

    original = Measurement(**original)
    future = Measurement(**future)
    present = Measurement(**present)
    past = Measurement(**past)

    assert original == future
    assert original == present
    assert original == past


def test_adding_source():
    headers = {'X-API-Key': os.environ.get('LINKA_MASTER_KEY')}
    source = {
        'name': 'test'
    }

    response = client.post(
        '/api/v1/sources', json=source, headers=headers
    )

    assert response.status_code == 200
