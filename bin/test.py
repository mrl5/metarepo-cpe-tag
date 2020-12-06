#!/usr/bin/env python3


import pop.hub


hub = pop.hub.Hub()
hub.pop.conf.integrate(["cpe_tag"], loader="yaml", roots=True)
hub.pop.sub.add(dyne_name="cpe_tag", omit_class=False)


def main(args):
    query_cpe_match = hub.cpe_tag.searchers.query_cpe_match
    return query_cpe_match('busybox:1.29.0')


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
