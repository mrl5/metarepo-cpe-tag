#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
from hashlib import sha256
from pathlib import Path
from sys import argv, exit, stdout
from urllib.parse import urlparse
from uuid import uuid4

from requests import get  # type: ignore

FILENAME = argv[0]
CPE_MATCH_URL = "https://nvd.nist.gov/feeds/json/cpematch/1.0"
CPE_MATCH_FEED_GZ = "nvdcpematch-1.0.json.gz"
CPE_MATCH_FEED_META = "nvdcpematch-1.0.meta"


def download_feed(destination: Path, filename=CPE_MATCH_FEED_GZ) -> None:
    url = f"{CPE_MATCH_URL}/{CPE_MATCH_FEED_GZ}"
    parsed_url = urlparse(url)
    download_loc = destination / filename
    print(f"Connecting to {parsed_url.netloc} ...")
    with get(url, stream=True) as r:
        r.raise_for_status()
        print(f"Downloading {CPE_MATCH_FEED_GZ} ...")
        with open(download_loc, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                stdout.write(".")
                stdout.flush()
                f.write(chunk)


def is_feed_latest(destination: Path) -> bool:
    print("Checking for updates ...")
    url = f"{CPE_MATCH_URL}/{CPE_MATCH_FEED_META}"
    parsed_url = urlparse(url)
    feed_loc = destination / CPE_MATCH_FEED_GZ

    print(f"Connecting to {parsed_url.netloc} ...")
    with get(url, stream=True) as r:
        print(f"Reading from {CPE_MATCH_FEED_META} ...")
        checksum_line = list(
            filter(lambda a: a.startswith("sha256"), r.text.splitlines())
        ).pop()
        remote_sha256sum = checksum_line.split(":").pop().lower()

    print("Comparing SHA256 checksums ... ")
    with gzip.open(feed_loc, "rb") as f:
        bytes = f.read()
        local_sha256sum = sha256(bytes).hexdigest()

    return remote_sha256sum == local_sha256sum


def update_feed(destination: Path) -> None:
    feed_loc = destination / CPE_MATCH_FEED_GZ
    tmp_filename = f"{CPE_MATCH_FEED_GZ}.{uuid4()}.tmp"
    download_feed(destination, filename=tmp_filename)
    feed_loc.unlink()
    (destination / tmp_filename).rename(feed_loc)


def run(args):
    if args[0] == "-h" or args[0] == "--help":
        help_msg = f"Usage: {FILENAME} path/to/download/dir"
        print(help_msg)
        return

    path = Path(args[0])
    if not path.is_dir():
        path.mkdir(mode=0o755, parents=True)

    if not (path / CPE_MATCH_FEED_GZ).is_file():
        download_feed(path)
        return

    print(f"Found {CPE_MATCH_FEED_GZ} on filesystem")
    if not is_feed_latest(path):
        print(f"Newer version of {CPE_MATCH_FEED_GZ} is available")
        update_feed(path)
    else:
        print("Everything up to date")


if __name__ == "__main__":
    args = argv[1:]
    if len(argv) != 2:
        exit("Expected only one arg")
    exit(run(args))
