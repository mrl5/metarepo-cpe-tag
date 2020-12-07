#!/usr/bin/env python3

import asyncio
from re import search, sub


def get_cpe_uri_from_json_line(hub, json_line: str) -> str:
    return sub(r",$", "", ":".join(json_line.split(":")[1:]).strip().replace('"', ""))


def safe_search(pattern: str, line: str) -> str:
    escaped = sub(r"[+]", "\\+", pattern)
    return search(escaped, line)


async def query_cpe_match(hub, quasi_cpe: str, feed=None) -> list:
    matches = []

    if quasi_cpe is None:
        return matches

    pattern = hub.cpe_tag.generators.convert_quasi_cpe_to_regex(quasi_cpe)
    if feed is None:
        feed_loc = hub.OPT.cpe_tag.cpe_match_feed
        proc = await asyncio.create_subprocess_shell(
            f"zcat {feed_loc} | grep {quasi_cpe}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        for line in stdout.decode("utf-8").splitlines():
            s = safe_search(pattern, line)
            if s is not None:
                matches.append(get_cpe_uri_from_json_line(hub, s.string))

    else:
        for line in feed:
            s = safe_search(pattern, line)
            if s is not None:
                matches.append(get_cpe_uri_from_json_line(hub, s.string))
    return list(set(matches))
