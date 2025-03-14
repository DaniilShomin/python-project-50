import json

import yaml
from yaml.loader import SafeLoader

from gendiff.diff_json import get_generated_diff_json
from gendiff.diff_plain import get_generated_diff_plain
from gendiff.diff_stylish import get_generated_diff


def generate_diff(filepath1, filepath2, format_name='stylish'):
    file1 = open_json_yaml(filepath1)
    file2 = open_json_yaml(filepath2)
    diff_file = ''
    if format_name == 'stylish' or not format_name:
        diff_file = get_generated_diff(file1, file2)
    elif format_name == 'plain':
        diff_file = get_generated_diff_plain(file1, file2)
        diff_file = diff_file.replace("'False'", 'false')
        diff_file = diff_file.replace("'True'", 'true')
        diff_file = diff_file.replace("'None'", 'null')
    elif format_name == 'json':
        diff_file = get_generated_diff_json(file1, file2)
    return diff_file


def open_json_yaml(filepath):
    if filepath.endswith('.json'):
        with open(filepath) as file:        
            return json.load(file)
    elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
        with open(filepath) as file: 
            return yaml.load(file, Loader=SafeLoader)