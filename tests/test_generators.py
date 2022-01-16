# IMPORTANT!
#
# this test suite ensures that JSON Schemas reposible for output contract
# (defined as schemas/tagged_*.schema.json) are respected by the codebase

import pytest

from cpe_tag.generators import tag_package_with_cpes, tag_packages_with_cpes
from cpe_tag.utils import get_tagged_batch_validator, get_tagged_package_validator

mock_nvdcpematch = [
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3976.1:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:android:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:linux:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:*:*:*"\n',
]


@pytest.mark.parametrize(
    "feed, package, expected",
    [
        (
            mock_nvdcpematch,
            {
                "name": "openssh",
                "versions": [
                    {"version": "7.5-r1", "quasi_cpe": ":openssh:7.5:::::::"},
                    {"version": "7.5_p1-r1", "quasi_cpe": ":openssh:7.5:p1::::::"},
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
        (
            mock_nvdcpematch,
            {
                "name": "firefox-bin",
                "versions": [
                    {"version": "83.0", "quasi_cpe": ":firefox:83.0:::::linux::"}
                ],
            },
            {
                "name": "firefox-bin",
                "versions": [
                    {
                        "version": "83.0",
                        "cpes": [
                            "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:*:*:*",
                            "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:linux:*:*",
                        ],
                    }
                ],
            },
        ),
    ],
)
def test_tag_package_with_cpes(feed, package, expected):
    result = tag_package_with_cpes(package, feed=feed)
    v = get_tagged_package_validator()
    v.validate(result)
    assert result["name"] == expected["name"]
    for v in result["versions"]:
        assert any(list(map(lambda x: x == v, expected["versions"]))) is True


def test_tag_packages_with_cpes():
    batch = [
        {
            "name": "openssh",
            "versions": [
                {"version": "7.5-r1", "quasi_cpe": ":openssh:7.5:::::::"},
                {"version": "7.5_p1-r1", "quasi_cpe": ":openssh:7.5:p1::::::"},
                {"version": "9999", "quasi_cpe": None},
                {"version": "9999"},
            ],
        },
        {
            "name": "firefox-bin",
            "versions": [{"version": "83.0", "quasi_cpe": ":firefox:83.0:::::linux::"}],
        },
    ]
    expected = [
        "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*",
        "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",
        "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*",
        "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:linux:*:*",
    ]

    result = tag_packages_with_cpes(batch, feed=mock_nvdcpematch)
    v = get_tagged_batch_validator()
    v.validate(result)  # type: ignore
    assert result.sort() == expected.sort()
