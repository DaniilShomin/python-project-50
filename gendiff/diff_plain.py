import itertools

from gendiff.interface import (
    get_action,
    get_key,
    get_value,
    get_value_after,
    get_value_before,
    is_nested,
)


def plain(data):  # noqa C901
    def iter_(value, pre_key=""):  # noqa C901
        
        lines = []

        for item in value:
            if not pre_key:
                match get_action(item):
                    case 'saved':
                        lines.append(iter_(get_value(item),
                                           f"Property '{get_key(item)}"))
                    case 'added':
                        lines.append(
                          f"Property '{get_key(item)}' was added with value: "
                          f"{get_value(item) if not is_nested(get_value(item))
                             else "[complex value]"}"
                        )
                    case 'removed':
                        lines.append(f"Property '{get_key(item)}' was removed")
                    case 'changed':
                        lines.append(
                            f"Property '{get_key(item)}' was updated. From "
                            f"{get_value_before(item) 
                               if not is_nested(get_value_before(item))
                               else "[complex value]"} to "
                            f"{get_value_after(item) 
                               if not is_nested(get_value_after(item))
                               else "[complex value]"}"
                        )
            else:
                match get_action(item):
                    case 'saved':
                        if is_nested(get_value(item)):
                            lines.append(iter_(get_value(item), 
                                               f"{pre_key}.{get_key(item)}"))
                    case 'added':
                        lines.append(
                          f"{pre_key}.{get_key(item)}' was added with value: "
                          f"{get_value(item) if not is_nested(get_value(item))
                                           else "[complex value]"}"
                        )
                    case 'removed':
                        lines.append(f"{pre_key}.{get_key(item)}' was removed")
                    case 'changed':
                        lines.append(
                            f"{pre_key}.{get_key(item)}' was updated. From "
                            f"{get_value_before(item) 
                               if not is_nested(get_value_before(item)) 
                               else "[complex value]"} to "
                            f"{get_value_after(item) 
                               if not is_nested(get_value_after(item)) 
                               else "[complex value]"}"
                        )
            lines = sorted(lines, key=lambda item: item.split()[1])
        result = itertools.chain(lines)    
        return '\n'.join(result)
    return iter_(data, '')