#!/usr/bin/env python3


import pop.hub
import pytest
from jsonschema import validate

from cpe_tag.cpe_tag.generators import convert_quasi_cpe_to_regex

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


mock_nvdcpematch = [
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3976.1:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*"\n',
]


quasi_cpe_testdata = [
    (
        {"product": "abc", "version": "1.2.3", "vendor": "foobar"},
        "foobar:abc:1.2.3:",
        "foobar:abc:1.2.3:[\\*\\-]",
    ),
    (
        {"product": "def", "version": "1.2.3", "update": "p2"},
        ":def:1.2.3:p2",
        ":def:1.2.3:(p2|[\\*])",
    ),
    ({"product": "ghi+", "version": "1337"}, ":ghi+:1337:", ":ghi\\+:1337:[\\*\\-]"),
]

tag_package_testdata = [
    (
        mock_nvdcpematch,
        {
            "name": "openssh",
            "versions": [
                {"version": "7.5-r1", "quasi_cpe": ":openssh:7.5:"},
                {"version": "7.5_p1-r1", "quasi_cpe": ":openssh:7.5:p1"},
                {"version": "9999", "quasi_cpe": None},
                {"version": "9999"},
            ],
        },
        {
            "name": "openssh",
            "versions": [
                {
                    "version": "7.5-r1",
                    "cpes": [
                        "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*",
                        "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",
                    ],
                },
                {
                    "version": "7.5_p1-r1",
                    "cpes": [
                        "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*",
                        "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*",
                    ],
                },
                {"version": "9999"},
                {"version": "9999"},
            ],
        },
    ),
]


@pytest.fixture(scope="function")
def get_quasi_cpe():
    return hub.cpe_tag.generators.get_quasi_cpe


@pytest.fixture(scope="function")
def tag_package_with_cpes():
    return hub.cpe_tag.generators.tag_package_with_cpes


def test_get_quasi_cpe_exceptions(get_quasi_cpe):
    with pytest.raises(hub.cpe_tag.errors.GeneratorError):
        get_quasi_cpe(wtf=1)
    with pytest.raises(hub.cpe_tag.errors.GeneratorError):
        get_quasi_cpe(product="a")
    with pytest.raises(hub.cpe_tag.errors.GeneratorError):
        get_quasi_cpe(version="1.2.3")


@pytest.mark.parametrize("params, expected, _", quasi_cpe_testdata)
def test_get_quasi_cpe(get_quasi_cpe, params, expected, _):
    assert get_quasi_cpe(**params) == expected


@pytest.mark.parametrize("_, quasi_cpe, expected", quasi_cpe_testdata)
def test_convert_quasi_cpe_to_regex(quasi_cpe, expected, _):
    assert convert_quasi_cpe_to_regex(quasi_cpe) == expected


@pytest.mark.parametrize("feed, package, expected", tag_package_testdata)
def test_tag_package_with_cpes(tag_package_with_cpes, package, expected, feed):
    result = tag_package_with_cpes(package, feed=feed)
    schema = hub.cpe_tag.utils.get_schema("tagged_package_json")
    validate(instance=result, schema=schema)
    assert result["name"] == expected["name"]
    for v in result["versions"]:
        assert any(list(map(lambda x: x == v, expected["versions"]))) is True
