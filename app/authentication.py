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
import json

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader, APIKey

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

keys = None
query = APIKeyHeader(name='X-API-Key', auto_error=False)


def get_all_keys():
    global keys

    if keys is not None:
        return keys

    sources_path = os.environ.get(
        'SOURCES_PATH', os.path.join(ROOT_DIR, 'data', 'sources.json.example'))
    with open(sources_path) as sources_json:
        keys = json.load(sources_json).get('keys', {})

    return keys


def get_current_key(key: APIKey = Security(query)):
    source = get_all_keys().get(key)

    if source is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )

    return source
