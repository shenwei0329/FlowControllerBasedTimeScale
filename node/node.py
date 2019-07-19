# -*- coding: UTF-8 -*-
#
#   The package for node
#

import time
import hashlib
import logging


class Node:

    def __init__(self, name):
        self.id = hashlib.sha1("%s" % time.time()).hexdigest()
        self.name = name

        logging.info("%s: <%s><%s>" % (__name__, str(self.id), self.name))

        self.function = None
        self.in_channel = []
        self.out_channel = []

    def add_in_channel(self, ch):
        self.in_channel.append(ch)

    def add_out_channel(self, ch):
        self.out_channel.append(ch)

    def add_function(self, func):
        self.function = func

    def _do_it(self, _event):

        _new_event = self.function(_event)

        logging.info("%s.%s >>> %s: %s" % (__name__, self.name, str(_new_event.time_scale), _new_event.data))

        if _new_event is not None:
            if len(self.out_channel) > 0:

                # 把处理结果往后传递
                for _oq in self.out_channel:
                    _oq.in_q(_new_event)

    def run(self):
        """
        To operate the  function of node.
        :return: Result of event.
        """

        if self.function is None:
            return

        if len(self.in_channel) == 0:
            """root node"""
            self._do_it(None)
            return

        for _q in self.in_channel:

            # to operate one event at one time.
            _event = _q.out_q()
            if _event is not None:
                self._do_it(_event)
