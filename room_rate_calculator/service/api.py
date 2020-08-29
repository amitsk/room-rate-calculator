# https://date.nager.at/Api

from datetime import date
from typing import Dict, Any, List, Mapping, NamedTuple

import requests
from collections import namedtuple

DATE_API_BASE_URL = "https://date.nager.at/api/v2/PublicHolidays"

Holiday = namedtuple("Holiday", ["date", "name"])


def get_public_holidays(dt: date) -> List[Holiday]:
    resp = requests.get(f"{DATE_API_BASE_URL}/{date.year}/US")
    if resp.status_code == 200:
        raw_json = resp.json()
        return [Holiday(row["date"], row["name"]) for row in raw_json if row["global"]]

    return []
