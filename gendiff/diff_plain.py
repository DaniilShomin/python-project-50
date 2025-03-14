import copy
import itertools


def get_generated_diff_plain(data, data2):  # noqa: C901
    copy_file2 = copy.deepcopy(data2)

    def iter(current_value, current_value2, pre_key=''):  # noqa: C901
        lines = []
        for key, val in current_value.items():            
            if not isinstance(val, dict):                              
                if pre_key:
                    if current_value2.get(key, 'not_key') != 'not_key':
                        if current_value[key] != current_value2[key]:
                            if not isinstance(current_value2[key], dict):
                                lines.append(
                                    f"{pre_key}.{key}' was updated. From "
                                    f'{current_value[key] 
                                       if isinstance(current_value[key], int) 
                                       else f"\'{current_value[key]}\'"} to '
                                    f'{current_value2[key]
                                       if isinstance(current_value2[key], int) 
                                       else f"\'{current_value2[key]}\'"}'
                                    )
                                current_value2.pop(key)
                            else:
                                lines.append(
                                    f"{pre_key}.{key}' was updated. From "
                                    f'{current_value[key] 
                                       if isinstance(current_value[key], int) 
                                       else f"\'{current_value[key]}\'"}'
                                    f" to [complex value]"
                                    )
                                current_value2.pop(key)
                        else:
                            current_value2.pop(key)
                    else:
                        lines.append(f"{pre_key}.{key}' was removed")
                else:
                    if current_value2.get(key, 'not_key') != 'not_key':
                        if current_value[key] != current_value2[key]:
                            lines.append(
                                f"Property '{key}' was updated. From "
                                f'{current_value[key] 
                                    if isinstance(current_value[key], int) 
                                    else f"\'{current_value[key]}\'"} to '
                                f'{current_value2[key]
                                    if isinstance(current_value2[key], int) 
                                    else f"\'{current_value2[key]}\'"}'
                                )
                            current_value2.pop(key)
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
                                f'{current_value2[key]
                                if isinstance(current_value2[key], int) 
                                else f"\'{current_value2[key]}\'"}'
                                )
                            current_value2.pop(key)
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
                                    f"with value: "
                                    f'{current_value2[key]
                                    if isinstance(current_value2[key], int) 
                                    else f"\'{current_value2[key]}\'"}'
                                    )
                            else:
                                lines.append(
                                    f"Property '{key}' was added "
                                    f"with value: "
                                    f'{current_value2[key]
                                    if isinstance(current_value2[key], int) 
                                    else f"\'{current_value2[key]}\'"}'
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