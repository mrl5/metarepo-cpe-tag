package_json_schema = {
    "title": "package",
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "package name"},
        "homepages": {
            "type": "array",
            "items": {"type": "string", "description": "project homepage"},
        },
        "versions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "version": {"type": "string", "description": "package version"},
                },
                "required": ["version"],
            },
        },
    },
    "required": ["name", "versions"],
}
