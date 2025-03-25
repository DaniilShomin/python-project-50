import itertools
import json


def plain(value):  # noqa: C901

    def iter_(current_value, pre_key=''):  # noqa: C901
        if not isinstance(current_value, list):
            return json.dumps(current_value)
        
        if pre_key == "complex":
            return "[complex value]"

        lines = []
        for item in current_value:
            if not pre_key:
                if item["type"] == "saved":
                    lines.append(
                        iter_(item["value"], f"Property '{item["key"]}"))
                elif item["type"] == "removed":
                    lines.append(f"Property '{item["key"]}' was removed")
                elif item["type"] == "added":
                    lines.append(
                        f"Property '{item["key"]}' was added with value: "
                        f"{iter_(item["value"], "complex")}")
            else:
                if item["type"] == "removed":
                    lines.append(f"{pre_key}.{item["key"]}' was removed")
                elif item["type"] == "changed":
                    lines.append(
                        f"{pre_key}.{item["key"]}' was updated. From "
                        f"{iter_(item["value"][0], "complex")} to "
                        f"{iter_(item["value"][1], "complex")}")
                elif item["type"] == "added":
                    lines.append(
                        f"{pre_key}.{item["key"]}' was added with value: "
                        f"{iter_(item["value"], "complex")}")
                elif item["type"] == "saved" \
                    and isinstance(item["value"], list):
                    lines.append(
                        iter_(item["value"], f"{pre_key}.{item["key"]}"))

            lines = sorted(lines, key=lambda item: item.split()[1])
        result = itertools.chain(lines)    
        return '\n'.join(result)

    return iter_(value, '').replace('"', "'")