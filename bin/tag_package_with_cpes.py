#!/usr/bin/env python3

import json

import pop.hub

hub = pop.hub.Hub()
hub.pop.conf.integrate(["cpe_tag"], loader="yaml", roots=True)
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


def main(args):
    package = json.loads(hub.OPT.cpe_tag.package_json)
    serialized = hub.cpe_tag.serializers.serialize_package_json(package)
    tagged = hub.cpe_tag.generators.tag_package_with_cpes(serialized)
    return json.dumps(tagged)


if __name__ == "__main__":
    import sys

    output = main(sys.argv[1:])
    print(output)
