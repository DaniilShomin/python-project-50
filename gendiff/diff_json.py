import json


def json_diff(value):
    return json.dumps(value, indent="  ", sort_keys=True)
