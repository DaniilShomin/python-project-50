import copy
import json


def get_generated_diff_json(data1, data2):  # noqa: C901
    copy_file2 = copy.deepcopy(data2)

    def iter(current_value, current_value2):  # noqa: C901
        result = {}
        for key, val in current_value.items():
            if not isinstance(val, dict):
                if current_value2.get(key, 'not_key') != 'not_key':
                    if current_value[key] == current_value2[key]:
                        result[key] = current_value2.pop(key)
            else:
                if current_value2.get(key, 'not_key') != 'not_key':
                    if not isinstance(current_value2[key], str):
                        result[key] = iter(current_value[key], 
                                           current_value2.pop(key))
            if list(current_value)[-1] == key:
                if len(current_value2) > 0:
                    for key, val in current_value2.items():
                        result[key] = val
        return result
    return json.dumps(iter(data1, copy_file2), indent=2, sort_keys=True)
