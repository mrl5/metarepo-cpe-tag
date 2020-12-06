#!/usr/bin/env python3


import pop.hub
import pytest

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


@pytest.fixture(scope="function")
def get_cpe_uri_from_json_line():
    return hub.cpe_tag.searchers.get_cpe_uri_from_json_line


def test_get_cpe_uri_from_json_line(get_cpe_uri_from_json_line):
    testdata = '      "cpe23Uri" : "cpe:2.3:a:busybox:busybox:1.29.0:*:*:*:*:*:*:*"\n'
    expected = "cpe:2.3:a:busybox:busybox:1.29.0:*:*:*:*:*:*:*"
    assert get_cpe_uri_from_json_line(testdata) == expected
