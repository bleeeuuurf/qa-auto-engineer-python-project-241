from gendiff.formatters.stylish import format_stylish
from gendiff.parser import parse_data


def build_diff(data1, data2):
    keys = sorted(set(data1) | set(data2))
    diff = []

    for key in keys:
        if key in data1 and key in data2:
            if data1[key] == data2[key]:
                diff.append(("unchanged", key, data1[key]))
            else:
                diff.extend((
                    ("removed", key, data1[key]),
                    ("added", key, data2[key]),
                ))
        elif key in data1:
            diff.append(("removed", key, data1[key]))
        else:
            diff.append(("added", key, data2[key]))

    return diff


def generate_diff(file_path1, file_path2, format_name="stylish"):
    data1 = parse_data(file_path1)
    data2 = parse_data(file_path2)

    diff = build_diff(data1, data2)

    if format_name == "stylish":
        return format_stylish(diff)

    raise ValueError(f"not usablr format: {format_name}")