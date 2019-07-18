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
        """
        To put a event into the queue.
        :param event:
        :return:
        """
        self.queue.append(event)

    def out_q(self):
        """
        To out a event from queue at one time.
        :return: one or none.
        """
        if len(self.queue) == 0:
            return None

        return self.queue.pop(0)

    def insert_q(self, event):
        """
        To insert a event into header of the queue.
        :param event: a event.
        :return:
        """
        self.queue.insert(0, event)

