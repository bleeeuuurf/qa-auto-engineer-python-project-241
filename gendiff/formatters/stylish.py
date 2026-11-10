def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def format_stylish(diff):
    lines = []

    for status, key, value in diff:
        if status == "unchanged":
            lines.append(f"    {key}: {format_value(value)}")
        elif status == "removed":
            lines.append(f"  - {key}: {format_value(value)}")
        elif status == "added":
            lines.append(f"  + {key}: {format_value(value)}")
        elif status == "updated":
            old_value, new_value = value
            lines.extend((
                f"  - {key}: {format_value(old_value)}",
                f"  + {key}: {format_value(new_value)}",
            ))

    return "{\n" + "\n".join(lines) + "\n}"