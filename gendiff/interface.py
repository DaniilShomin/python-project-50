from gendiff.constants import DICTIONARY


def corect_output(value):
    if not is_nested(value):        
        if DICTIONARY.get(value):
            return DICTIONARY[value]
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, int):
            return value
    else:
        return value


def get_value(data):
    if not is_nested(data):
        return data
    return corect_output(data["value"])


def get_action(data):
    return data["type"]


def get_key(data):
    return data["key"]


def is_nested(data):
    if isinstance(data, list):
        return True
    elif isinstance(data, dict):
        return True 
    return False


def get_value_before(data):
    return corect_output(get_value(data)[0])


def get_value_after(data):
    return corect_output(get_value(data)[1])