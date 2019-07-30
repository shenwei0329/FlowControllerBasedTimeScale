# -*- coding: UTF-8 -*-
#
#   The package for channel
#
#   通道可扩展远程传递：
#   1）通过网络传递事件管理信息
#   2）通过共享存储管理事件的数据
#
#

import time
import hashlib

import logging


class Channel:

    def __init__(self, name):
        self.id = hashlib.sha1("%s" % time.time()).hexdigest()
        self.name = name

        logging.info("%s: <%s><%s>" % (__name__, str(self.id), self.name))

        self.queue = []

    def get_name(self):
        return self.name

    def in_q(self, event):
        """
        To put a event into the queue.
        :param event:
        :return:
        """
        # print event
        # print(">>> in_q<%s>: %d, %f" % (self.name, event.get_time_scale(), event.get_data()["val"]))
        self.queue.append(event)

    def get_first(self):
        if len(self.queue) == 0:
            return None
        return self.queue[0]

    def out_q(self):
        """
        To out a event from queue at one time.
        :return: one or none.
        """
        if len(self.queue) == 0:
            return None
        _event = self.queue.pop(0)
        # print(">>> out_q: %s" % _event.get_data())
        return _event

    def insert_q(self, event):
        """
        To insert a event into header of the queue.
        :param event: a event.
        :return:
        """
        self.queue.insert(0, event)

    def get_size_q(self):
        return len(self.queue)

