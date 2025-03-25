import itertools
import json


def pref():
    return ['  ', '- ', '+ ']  


def stylish(value, count=1):
    prefix = pref()

    def iter_(current_value, depth):
        if not isinstance(current_value, list):
            return json.dumps(current_value)
        
        indent_size = depth + count
        deep_indent = indent_size + 1
        indent = indent_size * '  ' 
        current_indent = '  ' * depth
        lines = []
        for item in current_value:
            if item["type"] == "saved":
                lines.append(
                    f'{indent}{prefix[0]}{item["key"]}: '
                    f'{iter_(item["value"], deep_indent)}')
            elif item["type"] == "removed":
                lines.append(
                    f'{indent}{prefix[1]}{item["key"]}: '
                    f'{iter_(item["value"], deep_indent)}')
            elif item["type"] == "changed":
                lines.append(
                    f'{indent}{prefix[1]}{item["key"]}: '
                    f'{iter_(item["value"][0], deep_indent)}')
                lines.append(
                    f'{indent}{prefix[2]}{item["key"]}: '
                    f'{iter_(item["value"][1], deep_indent)}')
            elif item["type"] == "added":
                lines.append(
                    f'{indent}{prefix[2]}{item["key"]}: '
                    f'{iter_(item["value"], deep_indent)}')
            lines = sorted(
                lines, 
                key=lambda item: item.split(f'{indent}')[1].split(':')[0][2:]
                    if item.split(f'{indent}')[1] 
                    else item.split(f'{indent}')[2].split(':')[0]
                )
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)
    
    return iter_(value, 0).replace('"', '')