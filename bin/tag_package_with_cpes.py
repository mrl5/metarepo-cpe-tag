#!/usr/bin/env python3

import json

import pop.hub

hub = pop.hub.Hub()
hub.pop.conf.integrate(["cpe_tag"], loader="yaml", roots=True)
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


def main(args):
    package = {
        "name": "busybox",
        "versions": [{"version": "1.29.0"}, {"version": "9999"},],
        "description": "Utilities for rescue and embedded systems",
        "homepages": ["https://www.busybox.net/"],
        "licenses": ["GPL-2"],
    }
    serialized = hub.cpe_tag.serializers.serialize_package_json(package)
    tagged = hub.cpe_tag.generators.enrich_package_with_cpes(serialized)
    return json.dumps(tagged)


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv[1:]))
