import pytest

from cpe_tag.cpe import convert_quasi_cpe_to_regex, get_quasi_cpe
from cpe_tag.errors import GeneratorError


def test_get_quasi_cpe_exceptions():
    with pytest.raises(GeneratorError):
        get_quasi_cpe(wtf=1)
    with pytest.raises(GeneratorError):
        get_quasi_cpe(product="a")
    with pytest.raises(GeneratorError):
        get_quasi_cpe(version="1.2.3")


quasi_cpe_testdata = [
    (
        {"product": "abc", "version": "1.2.3", "vendor": "foobar"},
        "foobar:abc:1.2.3:::::linux::",
        "foobar:abc:1\\.2\\.3:[\\*\\-]:[^:]+:[^:]+:[^:]+:(linux|\\*):[^:]+:[^:]",
    ),
    (
        {"product": "def", "version": "1.2.3", "update": "p2"},
        ":def:1.2.3:p2::::linux::",
        ":def:1\\.2\\.3:(p2|\\*):[^:]+:[^:]+:[^:]+:(linux|\\*):[^:]+:[^:]",
    ),
    (
        {"product": "ghi+", "version": "1337"},
        ":ghi+:1337:::::linux::",
        ":ghi\\+:1337:[\\*\\-]:[^:]+:[^:]+:[^:]+:(linux|\\*):[^:]+:[^:]",
    ),
]


@pytest.mark.parametrize("params, expected, _", quasi_cpe_testdata)
def test_get_quasi_cpe(params, expected, _):
    assert get_quasi_cpe(**params) == expected


@pytest.mark.parametrize("_, quasi_cpe, expected", quasi_cpe_testdata)
def test_convert_quasi_cpe_to_regex(quasi_cpe, expected, _):
    assert convert_quasi_cpe_to_regex(quasi_cpe) == expected
