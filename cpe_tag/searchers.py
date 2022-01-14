# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio
import logging
from re import search, sub
from shlex import quote

from cpe_tag import conf
from cpe_tag.cpe import convert_quasi_cpe_to_regex


async def query_multi_cpe_match(pattern: str, feed=None) -> list:
    matches = []

    if feed is None:
        feed_loc = conf.DEFAULT_FEED_PATH
        feed = await get_feed(feed_loc, pattern)

    for line in feed:
        s = search(pattern, line)
        if s is not None:
            matches.append(get_cpe_uri_from_json_line(s.string))
    return list(set(matches))


async def query_cpe_match(quasi_cpe: str, feed=None) -> list:
    if quasi_cpe is None:
        return []

    matches = []
    pattern = convert_quasi_cpe_to_regex(quasi_cpe)

    if feed is None:
        feed_loc = conf.DEFAULT_FEED_PATH
        feed = await get_feed(feed_loc, pattern)

    for line in feed:
        s = search(pattern, line)
        if s is not None:
            matches.append(get_cpe_uri_from_json_line(s.string))
    return list(set(matches))


async def get_feed(feed_loc: str, quasi_cpe: str) -> list:
    shell_escaped_path = quote(feed_loc)
    shell_escaped_keyword = quote(quasi_cpe)
    proc = await asyncio.create_subprocess_shell(
        f"/usr/bin/zgrep -E {shell_escaped_keyword} {shell_escaped_path}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    log_error(quasi_cpe, stderr)
    return stdout.decode("utf-8").splitlines()


def get_cpe_uri_from_json_line(json_line: str) -> str:
    no_key = ":".join(json_line.split(":")[1:])
    no_white_chars = no_key.strip()
    no_quotes = no_white_chars.replace('"', "")
    no_trailing_comma = sub(r",$", "", no_quotes)
    final = no_trailing_comma
    return final


def log_error(quasi_cpe: str, stderr: bytes) -> None:
    err = stderr.decode("utf-8")
    if len(err) > 0:
        logging.error(f"[{quasi_cpe}] {err}")
