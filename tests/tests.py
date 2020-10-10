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

import sys

from fastapi.testclient import TestClient

sys.path.insert(1, 'src')  # noqa E402
from src import service

client = TestClient(service.app)


def test_record():
    measurements = [
        {
            'temperature': 0,
            'humidity': 0,
            'light': 0,
            'noise': 0,
            'quality': 0,
        }
    ]

    response = client.post('/api/v1/record', json=measurements)
    assert response.status_code == 200
