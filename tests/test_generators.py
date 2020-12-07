#!/usr/bin/env python3


import pop.hub
import pytest

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


testdata = [
    ({"product": "abc", "version": "1.2.3", "vendor": "foobar"}, "foobar:abc:1.2.3:", "foobar:abc:1.2.3:[\*\-]"),
    ({"product": "def", "version": "1.2.3", "update": "p2"}, ":def:1.2.3:p2", ":def:1.2.3:(p2|[\*])"),
    ({"product": "ghi", "version": "1337"}, ":ghi:1337:", ":ghi:1337:[\*\-]"),
]


@pytest.fixture(scope="function")
def get_quasi_cpe():
    return hub.cpe_tag.generators.get_quasi_cpe


@pytest.fixture(scope="function")
def convert_quasi_cpe_to_regex():
    return hub.cpe_tag.generators.convert_quasi_cpe_to_regex


def test_get_quasi_cpe_exceptions(get_quasi_cpe):
    with pytest.raises(hub.cpe_tag.errors.GeneratorError):
        get_quasi_cpe(wtf=1)
    with pytest.raises(hub.cpe_tag.errors.GeneratorError):
        get_quasi_cpe(product="a")
    with pytest.raises(hub.cpe_tag.errors.GeneratorError):
        get_quasi_cpe(version="1.2.3")


@pytest.mark.parametrize("params,expected, _", testdata)
def test_get_quasi_cpe(get_quasi_cpe, params, expected, _):
    assert get_quasi_cpe(**params) == expected


@pytest.mark.parametrize("_, quasi_cpe, expected", testdata)
def test_convert_quasi_cpe_to_regex(convert_quasi_cpe_to_regex, quasi_cpe,expected, _):
    assert convert_quasi_cpe_to_regex(quasi_cpe) == expected
