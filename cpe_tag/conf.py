from pathlib import Path


CONFIG = {
    "package": {"default": None, "help": "package name from meta-repo"},
    "version": {"default": None, "help": "version in funtoo format (e.g. 1.2_p1-r1)"},
    "cpe_match_feed": {
        "default": str(Path.home() / "feeds/json/nvdcpematch-1.0.json.gz"),
        "help": "location of NVD CPE Match Feed on filesystem",
    },
}

CLI_CONFIG = {
    "package": {"package": ["-p", "--package"], "os": "PACKAGE", "type": str},
    "version": {"version": ["-v", "--version"], "os": "VERSION", "type": str},
    "cpe_match_feed": {
        "cpe_match_feed": ["-f", "--cpe-match-feed"],
        "os": "CPE_MATCH_FEED",
        "type": str,
    },
}

DYNE = {"cpe_tag": ["cpe_tag"]}
