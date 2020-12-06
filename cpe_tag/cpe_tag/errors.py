#!/usr/bin/env python3


def __init__(hub):
    global HUB
    HUB = hub


class SerializeError(TypeError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg
