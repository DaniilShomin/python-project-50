import copy
import itertools
import json

import yaml
from yaml.loader import SafeLoader


def generate_diff(filepath1, filepath2, format_name='stylish'):
    file1 = open_json_yaml(filepath1)
    file2 = open_json_yaml(filepath2)
    diff_file = ''
    if format_name == 'stylish' or not format_name:
        diff_file = get_generated_diff(file1, file2, pref)
    elif format_name == 'plain':
        diff_file = get_generated_diff_plain(file1, file2)
        diff_file = diff_file.replace("'False'", 'false')
        diff_file = diff_file.replace("'True'", 'true')
        diff_file = diff_file.replace("'None'", 'null')
    return diff_file


def open_json_yaml(filepath):
    if filepath.endswith('.json'):
        with open(filepath) as file:        
            return json.load(file)
    elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
        with open(filepath) as file: 
            return yaml.load(file, Loader=SafeLoader)


def pref():
    return ['  ', '- ', '+ ']       
   

def get_generated_diff(data, data2, pref, count=1):  # noqa: C901
    copy_file2 = copy.deepcopy(data2)
    prefix = pref()

    def iter(current_value, current_value2, depth):  # noqa: C901
        if not isinstance(current_value, dict):
            return json.dumps(current_value)
        
        indent_size = depth + count
        deep_indent = indent_size + 1
        indent = indent_size * '  ' 
        current_indent = '  ' * depth
        lines = []

        if not current_value2:
            for key, val in current_value.items():
                lines.append(f'{indent}{prefix[0]}{key}: '
                             f'{iter(current_value[key], {}, deep_indent)}')

        else:
            for key, val in current_value.items():            
                if not isinstance(val, dict):
                    if current_value2.get(key):
                        if current_value[key] == current_value2[key]:
                            lines.append(f'{indent}{prefix[0]}{key}: '
                                         f'{json.dumps(current_value2.pop(key))}')
                        else:
                            if current_value[key] and current_value2[key]:
                                lines.append(f'{indent}{prefix[1]}{key}: '
                                             f'{json.dumps(current_value[key])}')
                                lines.append(f'{indent}{prefix[2]}{key}: '
                                             f'{json.dumps(current_value2.pop(key))}')
                            elif not current_value[key] and current_value2[key]:
                                lines.append(f'{indent}{prefix[1]}{key}:'
                                             f'{json.dumps(current_value[key])}')
                                lines.append(f'{indent}{prefix[2]}{key}: '
                                             f'{json.dumps(current_value2.pop(key))}')
                            elif current_value[key] and not current_value2[key]:
                                lines.append(f'{indent}{prefix[1]}{key}: '
                                             f'{json.dumps(current_value[key])}')
                                lines.append(f'{indent}{prefix[2]}{key}:'
                                             f'{json.dumps(current_value2.pop(key))}')
                            else:
                                lines.append(f'{indent}{prefix[1]}{key}:'
                                             f'{json.dumps(current_value[key])}')
                                lines.append(f'{indent}{prefix[2]}{key}:'
                                             f'{json.dumps(current_value2.pop(key))}')
                    else:
                        lines.append(
                            f'{indent}{prefix[1]}{key}: '
                            f'{json.dumps(current_value[key])}'
                            )                                                      
                else:
                    if (current_value2.get(key) and 
                        not isinstance(current_value2.get(key), str)):
                        lines.append(
                            f'{indent}{prefix[0]}{key}: '
                            f'{iter(current_value[key], 
                                    current_value2.pop(key), 
                                    deep_indent)}'
                            )
                    elif (current_value2.get(key) and 
                          isinstance(current_value2.get(key), str)):
                        lines.append(
                            f'{indent}{prefix[1]}{key}: '
                            f'{iter(current_value[key], {}, deep_indent)}'
                            )
                    else:
                        lines.append(
                            f'{indent}{prefix[1]}{key}: '
                            f'{iter(current_value[key], {}, deep_indent)}'
                            )                    
                if list(current_value)[-1] == key:
                    if len(current_value2) > 0:
                        for key in current_value2.keys():
                            lines.append(
                                f'{indent}{prefix[2]}{key}: '
                                f'{iter(current_value2[key], {}, deep_indent)}'
                                )
                    lines = sorted(
                        lines, key=lambda item: item.split(f'{indent}')[1].split(':')[0][2:]  # noqa: E501
                        if item.split(f'{indent}')[1] 
                        else item.split(f'{indent}')[2].split(':')[0]
                        )
        result = itertools.chain('{', lines, [current_indent + '}'])
        return '\n'.join(result)
    return iter(data, copy_file2, 0).replace('"', '')


def get_generated_diff_plain(data, data2):  # noqa: C901
    copy_file2 = copy.deepcopy(data2)

    def iter(current_value, current_value2, pre_key=''):  # noqa: C901
        lines = []
        for key, val in current_value.items():            
            if not isinstance(val, dict):                              
                if pre_key:
                    if current_value2.get(key, 'not_key') != 'not_key':
                        if current_value[key] != current_value2[key]:
                            lines.append(
                                f"{pre_key}.{key}' was updated. From "
                                f"'{current_value[key]}' to "
                                f"'{current_value2.pop(key)}'"
                                )
                        else:
                            current_value2.pop(key)
                    else:
                        lines.append(f"{pre_key}.{key}' was removed")
                else:
                    if current_value2.get(key, 'not_key') != 'not_key':
                        if current_value[key] != current_value2[key]:
                            lines.append(
                                f"Property '{key}' was updated. From "
                                f"'{current_value[key]}' to "
                                f"'{current_value2.pop(key)}'"
                                )
                        else:
                            current_value2.pop(key) 
                    else:
                        lines.append(f"Property '{key}' was removed")   
            else:
                if pre_key:
                    if current_value2.get(key):                        
                        if not isinstance(current_value2.get(key), str):
                            lines.append(iter(current_value[key], 
                                              current_value2.pop(key), 
                                              f"{pre_key}.{key}"))
                        else:
                            lines.append(
                                f"{pre_key}.{key}' was updated. "
                                f"From [complex value] to "
                                f"'{current_value2.pop(key)}'"
                                )
                    else:
                        lines.append(f"{pre_key}.{key}' was removed")
                else:
                    if current_value2.get(key):                        
                        if not isinstance(current_value2[key], str):
                            lines.append(
                                iter(current_value[key], 
                                     current_value2.pop(key), 
                                     f"Property '{key}")
                                     )
                    else:
                        lines.append(f"Property '{key}' was removed")
            if list(current_value)[-1] == key:
                if len(current_value2) > 0:
                    for key, val in current_value2.items():
                        if not isinstance(val, dict):
                            if pre_key:
                                lines.append(
                                    f"{pre_key}.{key}' was added "
                                    f"with value: '{current_value2[key]}'"
                                    )
                            else:
                                lines.append(
                                    f"Property '{key}' was added "
                                    f"with value: '{current_value2[key]}'"
                                    )
                        else:
                            if pre_key:
                                lines.append(
                                    f"{pre_key}.{key}' was added "
                                    "with value: [complex value]"
                                    )
                            else:
                                lines.append(
                                    f"Property '{key}' was added "
                                    "with value: [complex value]"
                                    )
                lines = sorted(lines, key=lambda item: item.split()[1])
        result = itertools.chain(lines)
        return '\n'.join(result)
    return iter(data, copy_file2, '')