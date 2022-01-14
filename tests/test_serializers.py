import pytest
from jsonschema import ValidationError

from cpe_tag.serializers import (
    serialize_package_json,
    serialize_package_name,
    serialize_version,
)

testnames = [
    ("a", tuple([None, "a"])),
    ("a-bin", tuple([None, "a"])),
    ("a-b", tuple([None, "a-b"])),
    ("a-b-bin", tuple([None, "a-b"])),
    ("google-a", tuple(["google", "a"])),
    ("google-a-bin", tuple(["google", "a"])),
    ("nicotine+", tuple([None, "nicotine+"])),
]

testversions = [
    ("1.2", tuple(["1.2", None])),
    ("1.2-r1", tuple(["1.2", None])),
    ("1.3_p1", tuple(["1.3", "p1"])),
    ("1.3_p1-r1", tuple(["1.3", "p1"])),
    ("9999", tuple([None, None])),
    (9999, tuple([None, None])),
    ("0", tuple([None, None])),
    (0, tuple([None, None])),
]

errordata = (
    {},
    {"name": "a"},
    {"versions": []},
    {"name": "a", "versions": 123},
    {"name": "a", "versions": [{"a": "b"}]},
)


@pytest.mark.parametrize("name, expected", testnames)
def test_serialize_package_name(name, expected):
    assert serialize_package_name(name) == expected


@pytest.mark.parametrize("funtoo_version, expected", testversions)
def test_serialize_version(funtoo_version, expected):
    assert serialize_version(funtoo_version) == expected


@pytest.mark.parametrize("package", errordata)
def test_serialize_package_json_exceptions(package):
    with pytest.raises(ValidationError):
        serialize_package_json(package)
