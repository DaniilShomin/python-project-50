import itertools
import json


def is_key(d, key):
    for k in d.keys():
        if k == key:
            return True
    return False


def plain(value):  # noqa: C901

    def iter_(current_value, pre_key=''):  # noqa: C901
        if not isinstance(current_value, dict):
            return json.dumps(current_value)

        lines = []
        for key, val in current_value.items():
            if not isinstance(val, dict):                              
                if pre_key:
                    if key[0] == '-':
                        if is_key(current_value, '+' + key[1:]):
                            lines.append(
                                f"{pre_key}.{key[2:]}' was updated. "
                                f"From {iter_(val)} to "
                                f"{iter_(current_value['+' + key[1:]])}")
                        else:
                            lines.append(f"{pre_key}.{key[2:]}' was removed")
                    elif key[0] == '+':
                        if not is_key(current_value, '-' + key[1:]):
                            if isinstance(val, dict):
                                lines.append(
                                    f"{pre_key}.{key[2:]}' was added "
                                    "with value: [complex value]")
                            else:
                                lines.append(
                                    f"{pre_key}.{key[2:]}' was added "
                                    f"with value: {iter_(val)}")
                else:
                    if key[0] == '-':
                        if is_key(current_value, '+' + key[1:]):
                            lines.append(
                                f"Property '{key[2:]}' was updated. "
                                f"From {iter_(val)} to "
                                f"{iter_(current_value['+' + key[1:]])}")
                        else:
                            lines.append(f"Property '{key[2:]}' was removed")
                    elif key[0] == '+':
                        if not is_key(current_value, '-' + key[1:]):
                            if isinstance(val, dict):
                                lines.append(
                                    f"Property '{key[2:]}' was added "
                                    "with value: [complex value]")
                            else:
                                lines.append(
                                    f"Property '{key[2:]}' was added "
                                    f"with value: {iter_(val)}")
            else:
                if pre_key:
                    if key[0] == '-':
                        if is_key(current_value, '+' + key[1:]):
                            if isinstance(val, dict):
                                lines.append(
                                    f"{pre_key}.{key[2:]}' was updated. "
                                    f"From [complex value] to "
                                    f"{iter_(current_value['+' + key[1:]])}")
                            else:
                                lines.append(
                                    f"{pre_key}.{key[2:]}' was updated. "
                                    f"From {iter_(val)} to "
                                    f"{iter_(current_value['+' + key[1:]])}")
                        else:
                            lines.append(f"{pre_key}.{key[2:]}' was removed")
                    elif key[0] == '+':
                        if not is_key(current_value, '-' + key[1:]):
                            lines.append(
                                f"{pre_key}.{key[2:]}' was added "
                                f"with value: [complex value]")
                    else:
                        lines.append(iter_(val, f"{pre_key}.{key[2:]}"))
                else:
                    if key[0] == '-':
                        if not is_key(current_value, '+' + key[1:]):
                            lines.append(
                                f"Property '{key[2:]}' was removed")
                    elif key[0] == '+':
                        if not is_key(current_value, '-' + key[1:]):
                            lines.append(
                                f"Property '{key[2:]}' was added "
                                "with value: [complex value]")
                    else: 
                        lines.append(iter_(val, f"Property '{key[2:]}"))
            lines = sorted(lines, key=lambda item: item.split()[1])
        result = itertools.chain(lines)    
        return '\n'.join(result)

    return iter_(value, '').replace('"', "'")