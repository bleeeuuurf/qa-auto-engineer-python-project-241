def format_value(value):
    if isinstance(value, str):
        return f"'{value}'"

    if value is None:
        return "null"

    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, (dict, list)):
        return "[complex value]"

    return str(value)


def format_plain(diff):
    lines = []

    for status, key, value in diff:
        if status == "removed":
            lines.append(f"Property '{key}' was removed")

        elif status == "added":
            lines.append(
                f"Property '{key}' was added with value: "
                f"{format_value(value)}"
            )

        elif status == "updated":
            old_value, new_value = value
            lines.append(
                f"Property '{key}' was updated. From "
                f"{format_value(old_value)} to {format_value(new_value)}"
            )

    return "\n".join(lines)