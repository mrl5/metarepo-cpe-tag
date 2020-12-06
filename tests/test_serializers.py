#!/usr/bin/env python3


import pop.hub
import pytest

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


errordata = (
    {},
    {"name": "a"},
    {"versions": []},
    {"name": "a", "versions": 123},
)

testdata = [
    (
        {"name": "a", "versions": ["1.2", "1.2-r1", "1.3_p1", "1.3_p1-r1", "9999", "0", 9999, 0]},
        ["a:1.2", "a:1.3:p1"],
    ),
    ({"name": "a-bin", "versions": ["1.2"]}, ["a:1.2"]),
    ({"name": "google-a", "versions": ["1.2"]}, ["google:a:1.2"]),
]


@pytest.fixture(scope="function")
def serialize_package_json():
    return hub.cpe_tag.serializers.serialize_package_json


@pytest.mark.parametrize("package", errordata)
def test_serialize_package_json_exceptions(serialize_package_json, package):
    with pytest.raises(hub.cpe_tag.errors.SerializeError):
        serialize_package_json(package)


@pytest.mark.parametrize("package,expected", testdata)
def test_serialize_package_json(serialize_package_json, package, expected):
    result = serialize_package_json(package)
    result.sort()
    expected.sort()
    assert result == expected
