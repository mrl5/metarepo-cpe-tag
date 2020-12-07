#!/usr/bin/env python3

import gzip
from re import search, sub


def get_cpe_uri_from_json_line(hub, json_line: str) -> str:
    return ':'.join(json_line.split(':')[1:]).strip().replace('"', "")


def safe_search(pattern: str, line: str) -> str:
    escaped = sub(r"[+]", "\\+", pattern)
    return search(escaped, line)


def query_cpe_match(hub, quasi_cpe: str, feed=None) -> list:
    matches = []

    if quasi_cpe is None:
        return matches

    pattern = hub.cpe_tag.generators.convert_quasi_cpe_to_regex(quasi_cpe)
    if feed is None:
        feed_loc = hub.OPT.cpe_tag.cpe_match_feed
        with gzip.open(feed_loc, "rt") as f:
            for line in f:
                s = safe_search(pattern, line)
                if s is not None:
                    matches.append(get_cpe_uri_from_json_line(hub, s.string))

    else:
        for line in feed:
            s = safe_search(pattern, line)
            if s is not None:
                matches.append(get_cpe_uri_from_json_line(hub, s.string))
    return list(set(matches))
