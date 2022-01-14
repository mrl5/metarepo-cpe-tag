import pytest
from jsonschema import validate

from cpe_tag.generators import tag_package_with_cpes
from cpe_tag.utils import get_schema

mock_nvdcpematch = [
    '      "cpe23Uri" : "cpe:2.3:a:google:chrome:80.0.3976.1:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:*:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:-:*:*:*:*:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:openbsd:openssh:7.5:p1:*:*:*:*:*:*"\n',
    '      "cpe23Uri" : "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:android:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:linux:*:*",\n',
    '      "cpe23Uri" : "cpe:2.3:a:mozilla:firefox:83.0:*:*:*:*:*:*:*"\n',
]

tag_package_testdata = [
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
            "versions": [{"version": "83.0", "quasi_cpe": ":firefox:83.0:::::linux::"}],
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
]


@pytest.mark.parametrize("feed, package, expected", tag_package_testdata)
def test_tag_package_with_cpes(package, expected, feed):
    result = tag_package_with_cpes(package, feed=feed)
    schema = get_schema("tagged_package_json")
    validate(instance=result, schema=schema)
    assert result["name"] == expected["name"]
    for v in result["versions"]:
        assert any(list(map(lambda x: x == v, expected["versions"]))) is True
