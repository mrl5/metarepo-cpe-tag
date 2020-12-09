#!/usr/bin/env python3

import asyncio
import logging
from re import search, sub

from .generators import convert_quasi_cpe_to_regex


def get_cpe_uri_from_json_line(json_line: str) -> str:
    return sub(r",$", "", ":".join(json_line.split(":")[1:]).strip().replace('"', ""))


def log_error(quasi_cpe, stderr):
    err = stderr.decode("utf-8")
    if len(err) > 0:
        logging.error(f"[{quasi_cpe}] {err}")


async def query_cpe_match(hub, quasi_cpe: str, feed=None) -> list:
    matches = []

    if quasi_cpe is None:
        return matches

    pattern = convert_quasi_cpe_to_regex(quasi_cpe)
    if feed is None:
        feed_loc = hub.OPT.cpe_tag.cpe_match_feed
        proc = await asyncio.create_subprocess_shell(
            f"/bin/zcat {feed_loc} | /bin/grep {quasi_cpe}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        for line in stdout.decode("utf-8").splitlines():
            s = search(pattern, line)
            if s is not None:
                matches.append(get_cpe_uri_from_json_line(s.string))
        log_error(quasi_cpe, stderr)
    else:
        for line in feed:
            s = search(pattern, line)
            if s is not None:
                matches.append(get_cpe_uri_from_json_line(s.string))
    return list(set(matches))
