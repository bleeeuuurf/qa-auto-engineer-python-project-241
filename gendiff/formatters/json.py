import json


def format_json(diff):
    statuses = ["added", "removed", "unchanged", "updated"]
    sorted_diff = sorted(
        diff,
        key=lambda item: statuses.index(item[0])
    )

    return json.dumps(sorted_diff, indent=4)