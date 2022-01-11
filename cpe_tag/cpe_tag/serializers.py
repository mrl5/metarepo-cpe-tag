#!/usr/bin/env python3

from re import match, sub
from typing import Optional, Tuple

VendorAndProduct = Tuple[Optional[str], str]
VersionAndUpdate = Tuple[Optional[str], Optional[str]]


def serialize_package_name(hub, funtoo_package: str) -> VendorAndProduct:
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


def serialize_version(hub, funtoo_version: str) -> VersionAndUpdate:
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


def serialize_package_json(hub, package: dict) -> dict:
    versions = package["versions"]
    vendor, product = serialize_package_name(hub, package["name"])
    for v in versions:
        version, update = serialize_version(hub, str(v["version"]))
        if version is not None:
            v["quasi_cpe"] = hub.cpe_tag.generators.get_quasi_cpe(
                vendor=vendor, product=product, version=version, update=update
            )
    return package
