#!/usr/bin/env python3

# Copyright 2021 Martín Abente Lahaye
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

import json
import requests
import argparse

from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta


def fetch(endpoint, source, days):
    now = datetime.now(timezone.utc)
    days_ago = now - timedelta(days=days)

    query = {
        "source": source,
        "start": days_ago.isoformat(),
        "end": now.isoformat(),
    }

    url = f"{endpoint}?{urlencode(query)}"
    response = requests.get(url)
    return response.json()


def export(data):
    csv = ""

    for index, entry in enumerate(data):
        if index == 0:
            row = [key for key in entry.keys()]
            row = ",".join(row)
            csv += f"{row}\n"

        row = [f"{json.dumps(entry[key])}" for key in entry.keys()]
        row = ",".join(row)
        csv += f"{row}\n"

    print(csv)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--days", type=int, required=True)

    args = parser.parse_args()
    data = fetch(args.endpoint, args.source, args.days)

    export(data)


if __name__ == "__main__":
    main()
