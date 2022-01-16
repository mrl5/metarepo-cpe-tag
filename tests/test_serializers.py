import pytest

from cpe_tag.serializers import serialize_package_name, serialize_version

testnames = [
    ("a", tuple(["", "a"])),
    ("a-bin", tuple(["", "a"])),
    ("a-b", tuple(["", "a-b"])),
    ("a-b-bin", tuple(["", "a-b"])),
    ("google-a", tuple(["google", "a"])),
    ("google-a-bin", tuple(["google", "a"])),
    ("nicotine+", tuple(["", "nicotine+"])),
]

testversions = [
    ("1.2", tuple(["1.2", ""])),
    ("1.2-r1", tuple(["1.2", ""])),
    ("1.3_p1", tuple(["1.3", "p1"])),
    ("1.3_p1-r1", tuple(["1.3", "p1"])),
    ("9999", tuple(["", ""])),
    (9999, tuple(["", ""])),
    ("0", tuple(["", ""])),
    (0, tuple(["", ""])),
]


@pytest.mark.parametrize("name, expected", testnames)
def test_serialize_package_name(name, expected):
    assert serialize_package_name(name) == expected


@pytest.mark.parametrize("funtoo_version, expected", testversions)
def test_serialize_version(funtoo_version, expected):
    assert serialize_version(funtoo_version) == expected
