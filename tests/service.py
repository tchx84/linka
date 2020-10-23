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

import os
import sys

from datetime import datetime
from urllib.parse import urlencode
from fastapi.testclient import TestClient

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

client = None
test_db_path = 'test.db'
sources_path = os.path.join(ROOT_DIR, 'data', 'sources.json.example')
headers = {'X-API-Key': 'bGlua2E6bGlua2E='}
measurements = [
    {
        'sensor': 'test',
        'source': 'test',
        'pm1dot0': 0.0,
        'pm2dot5': 0.0,
        'pm10': 0.0,
        'longitude': -25.194156,
        'latitude': -57.521369,
        'recorded': datetime.utcnow().isoformat(),
    },
]


def setup_module():
    global client

    if os.path.exists(test_db_path):
        os.unlink(test_db_path)
    os.environ['DATABASE_URL'] = f'sqlite:///./{test_db_path}'

    os.environ['SOURCES_PATH'] = f'{sources_path}'

    from alembic import config
    config.main(argv=['upgrade', 'head'])

    from app import service
    client = TestClient(service.app)


def teardown_module():
    if os.path.exists(test_db_path):
        os.unlink(test_db_path)


def test_record():
    response = client.post(
        '/api/v1/measurements',
        json=measurements,
        headers=headers)
    assert response.status_code == 200


def test_query():
    response = client.get('/api/v1/measurements')
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
        'longitude': -25.194156,
        'latitude': -57.521369,
        'distance': '100',
    }

    response = client.get(f'/api/v1/measurements?{urlencode(query)}')
    assert response.status_code == 200
    assert response.json() == measurements