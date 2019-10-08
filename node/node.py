# -*- coding: UTF-8 -*-
#
#   The package for node
#

import time
import hashlib
import logging
from event import event


class Node:

    def __init__(self, name):
        self.id = hashlib.sha1("%s" % time.time()).hexdigest()
        self.name = name
        self.synchronizer = None

        logging.info("%s: <%s><%s>" % (__name__, str(self.id), self.name))

        self.function = None
        self.in_channel = []
        self.out_channel = []
        self.sn = None

    def get_name(self):
        return self.name

    def add_synchronizer(self, sync):
        """
        添加输入同步器
        :param sync: 同步器
        :return:
        """
        self.synchronizer = sync
        """同步输入"""
        for _qn in self.in_channel:
            self.synchronizer.add_channel(_qn)

    def add_in_channel(self, ch):
        self.in_channel.append(ch)

    def add_out_channel(self, ch):
        self.out_channel.append(ch)

    def add_function(self, func):
        self.function = func

    def _do_it(self, _event, rg):
        """
        节点运行
        :param _event: 需要处理的输入事件组
        :param rg: 注册器
        :return:
        """

        """调用处理器"""
        _new_event = self.function(_event, self.sn)

        if _new_event is None:
            """无输出事件时"""
            return

        # logging.info("%s.%s >>> %s: %s" % (__name__, self.name, str(_new_event.time_scale), _new_event.data))
        # print _new_event.data

        if len(self.out_channel) > 0:
            _cnt = len(self.out_channel)
            """把处理结果往后传递"""
            for _oq in self.out_channel:
                """输出"""
                _q = rg.get_channel(_oq)
                _q.in_q(_new_event)
                _cnt -= 1
                if _cnt > 0:
                    """多个通道时，须复制事件"""
                    _new_event = _new_event.copy()

    def run(self, sn, rg):
        """
        To operate the  function of node.
        :param sn: 时间序列
        :param rg: 注册器
        :return: Result of event.
        """
        self.sn = sn
        if self.function is None:
            return

        if len(self.in_channel) == 0:
            """root node"""
            self._do_it(None, rg)
            return

        if (self.synchronizer is not None) and (not self.synchronizer.has_sync(rg)):
            """有输入同步器，且输入事件未同步时"""
            return

        _events = []
        for _iq in self.in_channel:

            _q = rg.get_channel(_iq)
            # to operate one event at one time.
            _event = _q.out_q()
            if _event is not None:
                _events.append(_event)
        if len(_events) > 0:
            self._do_it(_events, rg)

