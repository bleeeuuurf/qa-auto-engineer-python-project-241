import json
from pathlib import Path

import yaml


def parse_data(file_path):
    extension = Path(file_path).suffix

    with open(file_path) as file:
        if extension == ".json":
            return json.load(file)
        if extension in (".yaml", ".yml"):
            return yaml.safe_load(file)