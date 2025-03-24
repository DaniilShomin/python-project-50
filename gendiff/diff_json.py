import json


def json_diff(value):

    def iter_(current_value):
        if not isinstance(current_value, dict):
            return current_value
    
        result = {}
        for key, val in current_value.items():
            result[key[2:]] = iter_(val)
        return result

    return json.dumps(iter_(value), indent="  ", sort_keys=True)
