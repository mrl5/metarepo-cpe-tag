from pathlib import Path

CONFIG = {
    "package_json": {"default": None, "help": "funtoo package in JSON format"},
    "cpe_match_feed": {
        "default": str(Path.home() / "feeds/json/nvdcpematch-1.0.json.gz"),
        "help": "location of NVD CPE Match Feed on filesystem",
    },
}

CLI_CONFIG = {
    "package_json": {
        "package": ["-p", "--package-json"],
        "os": "PACKAGE",
        "type": str,
    },
    "cpe_match_feed": {
        "cpe_match_feed": ["-f", "--cpe-match-feed"],
        "os": "CPE_MATCH_FEED",
        "type": str,
    },
}

DYNE = {"cpe_tag": ["cpe_tag"]}
