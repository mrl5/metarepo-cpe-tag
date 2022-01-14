# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import astuple, dataclass
from re import escape

from cpe_tag.errors import GeneratorError


@dataclass
class WfnAttrs:
    vendor: str = ""
    product: str = ""
    version: str = ""
    update: str = ""
    edition: str = ""
    language: str = ""
    swedition: str = ""
    targetsw: str = "linux"
    targethw: str = ""
    other: str = ""


def throw_on_invalid_wfn_attrs(**wfn_attrs):
    try:
        assert ("product" in wfn_attrs) is True
        assert ("version" in wfn_attrs) is True
        assert len(wfn_attrs["product"]) > 0
        assert len(wfn_attrs["version"]) > 0
    except AssertionError:
        raise GeneratorError("missing required params")


def get_quasi_cpe(**wfn_attrs) -> str:
    throw_on_invalid_wfn_attrs(**wfn_attrs)
    w = WfnAttrs(**wfn_attrs)
    return ":".join(astuple(w))


def convert_quasi_cpe_to_regex(quasi_cpe: str) -> str:
    escaped = escape(quasi_cpe)
    w = WfnAttrs(*escaped.split(":"))
    w.update = "[\\*\\-]" if len(w.update) == 0 else f"({w.update}|\\*)"
    w.edition = "[^:]+" if len(w.edition) == 0 else f"({w.edition}|\\*)"
    w.language = "[^:]+" if len(w.language) == 0 else f"({w.language}|\\*)"
    w.swedition = "[^:]+" if len(w.swedition) == 0 else f"({w.swedition}|\\*)"
    w.targetsw = "[^:]+" if len(w.targetsw) == 0 else f"({w.targetsw}|\\*)"
    w.targethw = "[^:]+" if len(w.targethw) == 0 else f"({w.targethw}|\\*)"
    w.other = "[^:]" if len(w.other) == 0 else f"({w.other}|\\*)"
    return ":".join(astuple(w))
