# -*- coding: UTF-8 -*-
#
#   The package for channel
#

import time
import hashlib


class Channel:

    def __init__(self):
        self.id = hashlib.sha1("%s" % time.time()).hexdigest()
        self.queue = []

    def in_q(self, event):
        self.queue.append(event)

    def out_q(self):
        _event = self.queue.pop(0)

    def insert_q(self, event):
        self.queue.insert(0, event)

