import itertools
import json


def stylish(value, count=1):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return json.dumps(current_value)
        indent_size = depth + count
        deep_indent = indent_size + 1
        indent = indent_size * '  ' 
        current_indent = '  ' * depth
        lines = []
        for key, val in current_value.items():
            lines.append(f'{indent}{key}: {iter_(val, deep_indent)}')
            lines = sorted(
                lines, 
                key=lambda item: item.split(f'{indent}')[1].split(':')[0][2:]
                    if item.split(f'{indent}')[1] 
                    else item.split(f'{indent}')[2].split(':')[0]
                )
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)
    
    return iter_(value, 0).replace('"', '')