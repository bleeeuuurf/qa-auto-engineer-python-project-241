import json

from gendiff import generate_diff


def test_diff_with_same_files(tmp_path):
    data = {"name": "vika", "age": 25}

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data))
    file2.write_text(json.dumps(data))

    expected = (
        "{\n"
        "    age: 25\n"
        "    name: vika\n"
        "}"
    )

    assert generate_diff(file1, file2) == expected


def test_diff_with_different_values(tmp_path):
    data1 = {"name": "vika", "age": 25}
    data2 = {"name": "vika", "age": 26}

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = (
        "{\n"
        "  - age: 25\n"
        "  + age: 26\n"
        "    name: vika\n"
        "}"
    )

    assert generate_diff(file1, file2) == expected


def test_diff_with_different_keys(tmp_path):
    data1 = {"name": "vika", "hometown": "cheboksary"}
    data2 = {"name": "vika", "age": 25}

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = (
        "{\n"
        "  + age: 25\n"
        "  - hometown: cheboksary\n"
        "    name: vika\n"
        "}"
    )

    assert generate_diff(file1, file2) == expected


def test_diff_with_bool(tmp_path):
    data1 = {"argument": True}
    data2 = {"argument": False}

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = (
        "{\n"
        "  - argument: true\n"
        "  + argument: false\n"
        "}"
    )

    assert generate_diff(file1, file2) == expected


def test_diff_with_yaml():
    file1 = "tests/test_data/file1.yml"
    file2 = "tests/test_data/file2.yml"

    expected = (
        "{\n"
        "  - follow: false\n"
        "    host: hexlet.io\n"
        "  - proxy: 123.234.53.22\n"
        "  - timeout: 50\n"
        "  + timeout: 20\n"
        "  + verbose: true\n"
        "}"
    )

    assert generate_diff(file1, file2) == expected


def test_diff_with_plain_format(tmp_path):
    data1 = {
        "follow": False,
        "host": "hexlet.io",
        "proxy": "123.234.53.22",
        "timeout": 50,
    }
    data2 = {
        "host": "hexlet.io",
        "timeout": 20,
        "verbose": True,
    }

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = (
        "Property 'follow' was removed\n"
        "Property 'proxy' was removed\n"
        "Property 'timeout' was updated. From 50 to 20\n"
        "Property 'verbose' was added with value: true"
    )

    assert generate_diff(file1, file2, "plain") == expected


def test_plain_format_with_null_and_string(tmp_path):
    data1 = {
        "name": "vika",
        "nothing": None,
    }
    data2 = {
        "name": "masha",
        "active": True,
    }

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = (
        "Property 'active' was added with value: true\n"
        "Property 'name' was updated. From 'vika' to 'masha'\n"
        "Property 'nothing' was removed"
    )

    assert generate_diff(file1, file2, "plain") == expected


def test_plain_format_with_null(tmp_path):
    data1 = {"name": "vika"}
    data2 = {"name": "vika", "age": None}

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = "Property 'age' was added with value: null"

    assert generate_diff(file1, file2, "plain") == expected


def test_diff_with_json(tmp_path):
    data1 = {
        "name": "vika",
        "age": 25,
        "active_user": True,
    }
    data2 = {
        "name": "masha",
        "age": 25,
        "city": "Moscow",
    }

    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"

    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    expected = [
        ["added", "city", "Moscow"],
        ["removed", "active_user", True],
        ["unchanged", "age", 25],
        ["updated", "name", ["vika", "masha"]],
    ]

    result = generate_diff(file1, file2, "json")

    assert json.loads(result) == expected