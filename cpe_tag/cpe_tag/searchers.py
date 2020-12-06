#!/usr/bin/env python3

import gzip
from re import search


def get_cpe_uri_from_json_line(hub, json_line: str) -> str:
    return ':'.join(json_line.split(':')[1:]).strip().replace('"', "")


def query_cpe_match(hub, pattern: str) -> list:
    feed_loc = hub.OPT.cpe_tag.cpe_match_feed
    matches = []
    with gzip.open(feed_loc, "rt") as f:
        for line in f:
            s = search(pattern, line)
            if s is not None:
                matches.append(get_cpe_uri_from_json_line(hub, s.string))
    return matches
