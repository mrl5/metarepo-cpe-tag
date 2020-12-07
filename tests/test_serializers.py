#!/usr/bin/env python3


import pop.hub
import pytest

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


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


@pytest.fixture(scope="function")
def serialize_package_json():
    return hub.cpe_tag.serializers.serialize_package_json


@pytest.fixture(scope="function")
def serialize_package_name():
    return hub.cpe_tag.serializers.serialize_package_name


@pytest.fixture(scope="function")
def serialize_version():
    return hub.cpe_tag.serializers.serialize_version


@pytest.mark.parametrize("name, expected", testnames)
def test_serialize_package_name(serialize_package_name, name, expected):
    assert serialize_package_name(name) == expected


@pytest.mark.parametrize("funtoo_version, expected", testversions)
def test_serialize_version(serialize_version, funtoo_version, expected):
    assert serialize_version(funtoo_version) == expected


@pytest.mark.parametrize("package", errordata)
def test_serialize_package_json_exceptions(serialize_package_json, package):
    with pytest.raises(hub.cpe_tag.errors.SerializerError):
        serialize_package_json(package)
