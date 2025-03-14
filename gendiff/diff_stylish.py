import copy
import itertools
import json


def pref():
    return ['  ', '- ', '+ ']       
   

def get_generated_diff(data, data2, count=1):  # noqa: C901
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