#!/usr/bin/env python3


def __init__(hub):
    global HUB
    HUB = hub


class GeneratorError(TypeError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg


class SearcherError(AssertionError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg
