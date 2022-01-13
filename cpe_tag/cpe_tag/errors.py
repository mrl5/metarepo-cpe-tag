# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


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
