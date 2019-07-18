# -*- coding: UTF-8 -*-
#
#   The package for node
#

import time
import hashlib


class Node:

    def __init__(self):
        self.id = hashlib.sha1("%s" % time.time()).hexdigest()
        self.function = None
        self.in_channel = None
        self.out_channel = []

    def add_in_channel(self, ch):
        self.in_channel = ch

    def add_out_channel(self, ch):
        self.out_channel.append(ch)

    def add_function(self, func):
        self.function = func

    def run(self):
        if self.function is None:
            return
        if self.in_channel is None:
            return
        _event = self.in_channel.out_q()
        _new_event = self.function(_event)
        if (_new_event is not None) and (len(self.out_channel) > 0):
            for _q in self.out_channel:
                _q.in_q(_new_event)

