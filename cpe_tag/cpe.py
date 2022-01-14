# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from re import escape

from cpe_tag.errors import GeneratorError

# todo: use dataclass


def get_quasi_cpe(**wfn_attrs) -> str:
    throw_on_invalid_wfn_attrs(**wfn_attrs)

    vendor = (
        wfn_attrs["vendor"]
        if "vendor" in wfn_attrs and wfn_attrs["vendor"] is not None
        else ""
    )
    product = (
        wfn_attrs["product"]
        if "product" in wfn_attrs and wfn_attrs["product"] is not None
        else ""
    )
    version = (
        wfn_attrs["version"]
        if "version" in wfn_attrs and wfn_attrs["version"] is not None
        else ""
    )
    update = (
        wfn_attrs["update"]
        if "update" in wfn_attrs and wfn_attrs["update"] is not None
        else ""
    )
    edition = (
        wfn_attrs["edition"]
        if "edition" in wfn_attrs and wfn_attrs["edition"] is not None
        else ""
    )
    language = (
        wfn_attrs["language"]
        if "language" in wfn_attrs and wfn_attrs["language"] is not None
        else ""
    )
    swedition = (
        wfn_attrs["swedition"]
        if "swedition" in wfn_attrs and wfn_attrs["swedition"] is not None
        else ""
    )
    targetsw = (
        wfn_attrs["targetsw"]
        if "targetsw" in wfn_attrs and wfn_attrs["targetsw"] is not None
        else "linux"
    )
    targethw = (
        wfn_attrs["targethw"]
        if "targethw" in wfn_attrs and wfn_attrs["targethw"] is not None
        else ""
    )
    other = (
        wfn_attrs["other"]
        if "other" in wfn_attrs and wfn_attrs["other"] is not None
        else ""
    )

    parts = [
        vendor,
        product,
        version,
        update,
        edition,
        language,
        swedition,
        targetsw,
        targethw,
        other,
    ]
    return ":".join(parts)


def convert_quasi_cpe_to_regex(quasi_cpe: str) -> str:
    escaped = escape(quasi_cpe)
    (
        vendor,
        product,
        version,
        update,
        edition,
        language,
        swedition,
        targetsw,
        targethw,
        other,
    ) = escaped.split(":")
    update = "[\\*\\-]" if len(update) == 0 else f"({update}|\\*)"
    edition = "[^:]+" if len(edition) == 0 else f"({edition}|\\*)"
    language = "[^:]+" if len(language) == 0 else f"({language}|\\*)"
    swedition = "[^:]+" if len(swedition) == 0 else f"({swedition}|\\*)"
    targetsw = "[^:]+" if len(targetsw) == 0 else f"({targetsw}|\\*)"
    targethw = "[^:]+" if len(targethw) == 0 else f"({targethw}|\\*)"
    other = "[^:]" if len(other) == 0 else f"({other}|\\*)"
    parts = [
        vendor,
        product,
        version,
        update,
        edition,
        language,
        swedition,
        targetsw,
        targethw,
        other,
    ]
    return ":".join(parts)


def throw_on_invalid_wfn_attrs(**wfn_attrs):
    try:
        assert ("product" in wfn_attrs) is True
        assert ("version" in wfn_attrs) is True
        assert len(wfn_attrs["product"]) > 0
        assert len(wfn_attrs["version"]) > 0
    except AssertionError:
        raise GeneratorError("missing required params")
