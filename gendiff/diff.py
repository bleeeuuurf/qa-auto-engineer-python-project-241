from gendiff.parser import parse_json


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def generate_diff(file_path1, file_path2):
    data1 = parse_json(file_path1)
    data2 = parse_json(file_path2)

    keys = sorted(set(data1) | set(data2))
    lines = []

    for key in keys:
        if key in data1 and key in data2:
            if data1[key] == data2[key]:
                lines.append(f"    {key}: {format_value(data1[key])}")
            else:
                lines.extend((
                    f"  - {key}: {format_value(data1[key])}",
                    f"  + {key}: {format_value(data2[key])}",
                ))
        elif key in data1:
            lines.append(f"  - {key}: {format_value(data1[key])}")
        else:
            lines.append(f"  + {key}: {format_value(data2[key])}")

    return "{\n" + "\n".join(lines) + "\n}"
