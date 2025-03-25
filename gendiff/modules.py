import copy
import json

import yaml
from yaml.loader import SafeLoader

from gendiff.diff_json import json_diff
from gendiff.diff_plain import plain
from gendiff.diff_stylish import stylish


def generate_diff(filepath1, filepath2, format_name='stylish'):
    file1 = open_json_yaml(filepath1)
    file2 = open_json_yaml(filepath2)
    diff_file = get_generated_diff(file1, file2)
    if format_name == 'stylish' or not format_name:
        return stylish(diff_file)
    elif format_name == 'plain':
        return plain(diff_file)
    elif format_name == 'json':
        return json_diff(diff_file)


def open_json_yaml(filepath):
    if filepath.endswith('.json'):
        with open(filepath) as file:
            return json.load(file)
    elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
        with open(filepath) as file: 
            return yaml.load(file, Loader=SafeLoader)


def get_generated_diff(data, data2):  # noqa: C901

    copy_file2 = copy.deepcopy(data2)
    action = ['added', 'removed', 'changed', 'saved']

    def iter(current_value, current_value2={}):  # noqa: C901
        if not isinstance(current_value, dict):
            return current_value
                
        gen_diff = []

        if not current_value2:
            for key, val in current_value.items():
                gen_diff.append({
                    "key": key, 
                    "type": action[3], 
                    "value": iter(val)})

        else:
            for key, val in current_value.items():
                if not isinstance(val, dict):
                    if current_value2.get(key, 'not_key') != 'not_key':
                        if current_value[key] == current_value2[key]:
                            gen_diff.append({
                                "key": key, 
                                "type": action[3], 
                                "value": iter(current_value2.pop(key))}) 
                        else:
                            gen_diff.append({
                                "key": key, 
                                "type": action[2], 
                                "value": [iter(current_value[key]), 
                                          iter(current_value2.pop(key))]})
                    else:
                        gen_diff.append({
                            "key": key, 
                            "type": action[1], 
                            "value": iter(current_value[key])})
                else:
                    if (current_value2.get(key, 'not_key') != 'not_key' and
                        not isinstance(current_value2.get(key), str)):
                        gen_diff.append({
                            "key": key, 
                            "type": action[3], 
                            "value": iter(current_value[key], 
                                          current_value2.pop(key))})
                    elif (current_value2.get(key, 'not_key') != 'not_key' and
                          isinstance(current_value2.get(key), str)):
                        gen_diff.append({
                            "key": key, 
                            "type": action[2], 
                            "value": [iter(current_value[key]), 
                                      iter(current_value2.pop(key))]})
                    else:
                        gen_diff.append({
                            "key": key, 
                            "type": action[1], 
                            "value": iter(current_value[key])})
                if list(current_value)[-1] == key:
                    if len(current_value2) > 0:
                        for key in current_value2.keys():
                            gen_diff.append({
                                "key": key, 
                                "type": action[0], 
                                "value": iter(current_value2[key])})

        return gen_diff
    return iter(data, copy_file2)