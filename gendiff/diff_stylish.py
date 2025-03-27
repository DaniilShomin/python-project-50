import itertools

from gendiff.interface import (
    get_action,
    get_key,
    get_value,
    get_value_after,
    get_value_before,
    is_nested,
)


def pref():
    return ['  ', '- ', '+ ']  


def stylish(data, count=1):
    prefix = pref()

    def iter_(value, depth):
        if not is_nested(value):
            return get_value(value)
        
        indent_size = depth + count
        deep_indent = indent_size + 1
        indent = indent_size * '  ' 
        current_indent = '  ' * depth
        lines = []
        for item in value:
            match get_action(item):
                case 'saved':
                    lines.append(
                        f'{indent}{prefix[0]}{get_key(item)}: '
                        f'{iter_(get_value(item), deep_indent)}')
                case 'removed':
                    lines.append(
                        f'{indent}{prefix[1]}{get_key(item)}: '
                        f'{iter_(get_value(item), deep_indent)}')
                case 'changed':
                    lines.append(
                        f'{indent}{prefix[1]}{get_key(item)}: '
                        f'{iter_(get_value_before(item), deep_indent)}')
                    lines.append(
                        f'{indent}{prefix[2]}{get_key(item)}: '
                        f'{iter_(get_value_after(item), deep_indent)}')
                case 'added':
                    lines.append(
                        f'{indent}{prefix[2]}{get_key(item)}: '
                        f'{iter_(get_value(item), deep_indent)}')
            lines = sorted(
                lines, 
                key=lambda item: item.split(f'{indent}')[1].split(':')[0][2:]
                    if item.split(f'{indent}')[1] 
                    else item.split(f'{indent}')[2].split(':')[0]
                )
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)
    
    return iter_(data, 0).replace("'", '')