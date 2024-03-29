# -*- coding: UTF-8 -*-
#
#   The package for System
#   ============================
#   系统
#
#   系统，是一个独立的运行机制，由一组通过通道互相关联的节点组成，用于完整地处理输入事件并产生结果输出。
#   一个独立系统，是一个具有前、后端节点的自发产生输入事件处理系统，其输出结果由后端节点展示和或持久化保持。
#   一个复合系统，是由多个系统组成，系统之间通过通道连接。
#

from register import register
from node import node
from synchronizer import synchronizer
from channel import channel
from timesequence import timesequence
from concurrent.futures import ThreadPoolExecutor


class System:

    def __init__(self, init_police):
        self.name = init_police['name']
        self.structure = init_police['structure']
        """每个系统都具有自己的命名管理"""
        self.R = register.Register()
        """创建一个系统机制"""
        self._construct()
        self.sn = None
        self.Ts = timesequence.TimeSequence(time_policy=init_police['timer_police'])

    def _construct(self):
        """
        构建系统
        :return:
        """
        """1)创建通道"""
        for _ch in self.structure["channel"]:
            _c = channel.Channel(_ch)
            self.R.add_channel(_c)

        """2)创建节点"""
        for _nd in self.structure["node"]:
            _n = node.Node(_nd)
            _n.add_function(self.structure["node"][_nd]["function"])
            self.R.add_node(_n)

            """创建输入通道"""
            if "input" in self.structure["node"][_nd]:
                for _ch in self.structure["node"][_nd]["input"]:
                    _n.add_in_channel(_ch)

            """创建输出通道"""
            if "output" in self.structure["node"][_nd]:
                for _ch in self.structure["node"][_nd]["output"]:
                    _n.add_out_channel(_ch)
                    if "init" in self.structure["node"][_nd]:
                        _events = self.structure["node"][_nd]["init"]()
                        _q = self.R.get_channel(_ch)
                        for _e in _events:
                            _q.in_q(_e)

            """创建同步器"""
            if "synchronizer" in self.structure["node"][_nd]:
                if self.structure["node"][_nd]["synchronizer"]:
                    _sync = synchronizer.Synchronizer()
                    _n.add_synchronizer(_sync)

    def run(self):
        self.sn = self.Ts.wait()
        _link = self.R.get_node_list()
        with ThreadPoolExecutor(max_workers=6) as executor:
            [executor.submit(_link[_n].run(self.sn, self.R)) for _n in _link]


