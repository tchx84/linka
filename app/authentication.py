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

import hashlib

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader, APIKey

from .db import db
from . import models


query = APIKeyHeader(name='X-API-Key', auto_error=False)
InvalidAPIKey = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials"
)


async def validate_api_key(api_key: APIKey = Security(query)):
    if not api_key:
        raise InvalidAPIKey

    try:
        prefix, raw_api_key = api_key.split(".")
    except ValueError:
        raise InvalidAPIKey

    api_key_hash = hashlib.sha256(raw_api_key.encode('utf-8')).hexdigest()
    key = f"{prefix}.{api_key_hash}"

    api_keys = await models.APIKey.get_all_keys(db)
    if key not in api_keys:
        raise InvalidAPIKey
