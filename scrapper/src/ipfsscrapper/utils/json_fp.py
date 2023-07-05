import json
import logging
from typing import Any


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def log_json(obj: Any):
    logging.info(json.dumps(obj, indent=2))
