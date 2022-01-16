from contextlib import contextmanager

import pytest
from jsonschema import ValidationError

from cpe_tag.utils import validate_batch, validate_package


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "package, expectation",
    [
        ({"name": "a", "versions": [{"version": "1.2.3"}]}, does_not_raise()),
        ({"name": "a", "versions": "1.2.3"}, pytest.raises(ValidationError)),
        ({"name": "a", "versions": [{}]}, pytest.raises(ValidationError)),
        (
            [{"name": "a", "versions": [{"version": "1.2.3"}]}],
            pytest.raises(ValidationError),
        ),
    ],
)
def test_validate_package(package, expectation):
    with expectation:
        validate_package(package)


@pytest.mark.parametrize(
    "batch, expectation",
    (
        ([{"name": "a", "versions": [{"version": "1.2.3"}]}], does_not_raise()),
        (
            {"name": "a", "versions": [{"version": "1.2.3"}]},
            pytest.raises(ValidationError),
        ),
    ),
)
def test_validate_batch(batch, expectation):
    with expectation:
        validate_batch(batch)
