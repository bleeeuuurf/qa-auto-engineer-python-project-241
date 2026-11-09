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