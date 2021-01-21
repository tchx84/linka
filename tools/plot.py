#!/usr/bin/env python3

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

import dateutil
import requests
import argparse
import pandas as pd
import matplotlib.pyplot as plt

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


def plot(data, output, visualize):
    frame = {
        "PM2.5": [],
        "date": [],
    }
    for entry in data:
        frame["PM2.5"].append(entry["pm2dot5"])
        frame["date"].append(dateutil.parser.parse(entry["recorded"]))

    df = pd.DataFrame(frame)
    df.plot(kind="line", x="date", y="PM2.5")
    plt.savefig(output)

    if visualize is True:
        plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--days", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--visualize", action="store_true", default=False)

    args = parser.parse_args()
    data = fetch(args.endpoint, args.source, args.days)
    plot(data, args.output, args.visualize)


if __name__ == "__main__":
    main()
