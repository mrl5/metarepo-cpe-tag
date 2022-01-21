# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from re import match, sub
from typing import Tuple

from cpe_tag.conf import KNOWN_VENDORS
from cpe_tag.cpe import get_quasi_cpe

VendorAndProduct = Tuple[str, str]
VersionAndUpdate = Tuple[str, str]


def serialize_package_json(package: dict) -> dict:
    versions = package["versions"]
    vendor, product = serialize_package_name(package["name"])
    for v in versions:
        version, update = serialize_version(str(v["version"]))
        if len(version):
            v["quasi_cpe"] = get_quasi_cpe(
                vendor=vendor, product=product, version=version, update=update
            )
    return package


def serialize_package_name(funtoo_package: str) -> VendorAndProduct:
    result = match(rf"^({'|'.join(KNOWN_VENDORS)})(.+)", funtoo_package)

    if result is None:
        vendor = ""
        product = funtoo_package
    else:
        vendor, product = result.groups()
        product = sub(r"^-", "", product)

    product = sub(r"-bin$", "", product)
    return vendor, product


def serialize_version(funtoo_version: str) -> VersionAndUpdate:
    funtoo_version = str(funtoo_version) if funtoo_version is not None else ""
    if funtoo_version == "0" or funtoo_version == "9999":
        return "", ""

    try:
        version, update = funtoo_version.split("_")
    except ValueError:
        version = funtoo_version
        update = ""

    return strip_revision(version), strip_revision(update)


def strip_revision(x: str) -> str:
    if len(x):
        return sub(r"-r[0-9]{1}$", "", x)
    return ""
