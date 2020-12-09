#!/usr/bin/env python3


import pop.hub
import pytest

from cpe_tag.cpe_tag.searchers import get_cpe_uri_from_json_line

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


mock_nvdcpematch = [
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3976.1:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3977.0:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3977.1:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3987.87:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:test:nicotine+:13.37:-:*:*:*:*:*:*"\n',
]

testdata = [
    (
        mock_nvdcpematch,
        "google:chrome:80.0.3987.87:",
        ["cpe:2.3:a:google:chrome:80.0.3987.87:*:*:*:*:*:*:*"],
    ),
    (
        mock_nvdcpematch,
        ":openssh:7.5:",
        [
            "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*",
            "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",
        ],
    ),
    (
        mock_nvdcpematch,
        ":openssh:7.5:p1",
        [
            "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*",
            "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*",
        ],
    ),
    (
        mock_nvdcpematch,
        ":nicotine+:13.37:",
        ["cpe:2.3:a:test:nicotine+:13.37:-:*:*:*:*:*:*"],
    ),
    (mock_nvdcpematch, None, [],),
]


@pytest.fixture(scope="function")
def query_cpe_match():
    return hub.cpe_tag.searchers.query_cpe_match


def test_get_cpe_uri_from_json_line():
    testdata = '      "cpe23Uri" : "cpe:2.3:a:busybox:busybox:1.29.0:*:*:*:*:*:*:*"\n'
    expected = "cpe:2.3:a:busybox:busybox:1.29.0:*:*:*:*:*:*:*"
    assert get_cpe_uri_from_json_line(testdata) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("feed,pattern,expected", testdata)
async def test_query_cpe_match(query_cpe_match, feed, pattern, expected):
    result = await query_cpe_match(pattern, feed=feed)
    result.sort()
    expected.sort()
    assert result == expected
