# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from re import match, sub
from typing import Optional, Tuple

from jsonschema import validate

from cpe_tag.cpe import get_quasi_cpe
from cpe_tag.utils import get_schema

VendorAndProduct = Tuple[Optional[str], str]
VersionAndUpdate = Tuple[Optional[str], Optional[str]]


def serialize_package_name(funtoo_package: str) -> VendorAndProduct:
    known_vendors = ["google", "oracle"]

    result = match(rf"^({'|'.join(known_vendors)})(.+)", funtoo_package)

    if result is None:
        vendor = None
        product = funtoo_package
    else:
        vendor, product = result.groups()
        product = sub(r"^-", "", product)

    product = sub(r"-bin$", "", product)
    return vendor, product


def strip_revision(x: Optional[str]) -> Optional[str]:
    if x is not None:
        return sub(r"-r[0-9]{1}$", "", x)
    return None


def serialize_version(funtoo_version: str) -> VersionAndUpdate:
    funtoo_version = (
        str(funtoo_version) if funtoo_version is not None else funtoo_version
    )
    if funtoo_version == "0" or funtoo_version == "9999":
        return None, None

    try:
        version, update = funtoo_version.split("_")
    except ValueError:
        version = funtoo_version
        update = None

    return strip_revision(version), strip_revision(update)


def serialize_package_json(package: dict) -> dict:
    throw_on_invalid_package(package)

    versions = package["versions"]
    vendor, product = serialize_package_name(package["name"])
    for v in versions:
        version, update = serialize_version(str(v["version"]))
        if version is not None:
            v["quasi_cpe"] = get_quasi_cpe(
                vendor=vendor, product=product, version=version, update=update
            )
    return package


def throw_on_invalid_package(package: dict):
    package_json_schema = get_schema("package_json")
    validate(instance=package, schema=package_json_schema)
