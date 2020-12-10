#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import pop.hub


hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag")
hub.cpe_tag.init.cli()


def main():
    package = json.loads(hub.OPT.cpe_tag.package_json)
    serialized = hub.cpe_tag.serializers.serialize_package_json(package)
    tagged = hub.cpe_tag.generators.tag_package_with_cpes(serialized)
    return json.dumps(tagged)


print(main())
