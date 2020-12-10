from pathlib import Path

CLI_CONFIG = {
    "package_json": {
        "positional": True,
    },
    "cpe_match_feed": {
        "cpe_match_feed": ["-f", "--cpe-match-feed"],
        "os": "CPE_MATCH_FEED",
        "type": str,
    },
}

CONFIG = {
    "cpe_match_feed": {
        "default": str(Path.home() / "feeds/json/nvdcpematch-1.0.json.gz"),
        "help": "location of NVD CPE Match Feed on filesystem",
    },
}

SUBCOMMANDS = {}

DYNE = {
    "cpe_tag": ["cpe_tag"],
}
