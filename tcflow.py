# -*- coding: UTF-8 -*-
#
#   TCFlow
#   ======
#   A Flow Control system based on Time scale
#
#   基于时标的流控制系统体系
#   核心单元：节点Node、通道Channel
#
#

import time
import logging
from node import node
from channel import channel
from register import register
from synchronizer import synchronizer

from application import system_a

logging.basicConfig(filename="tcflow.log",
                    filemode="w",
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S",
                    encoding="utf-8",
                    level=logging.DEBUG)


def main():

    logging.info("<%s> Starting" % __name__)

    # 创建注册器实体
    register.R = register.Register()

    """构建系统"""
    """1)创建节点"""
    for _nd in system_a.system["node"]:
        _n = node.Node(_nd)
        _n.add_function(system_a.system["node"][_nd]["function"])
        register.R.add_node(_n)

        """创建输入通道"""
        if "input" in system_a.system["node"][_nd]:
            for _ch in system_a.system["node"][_nd]["input"]:
                _n.add_in_channel(_ch)

        """创建输出通道"""
        if "output" in system_a.system["node"][_nd]:
            for _ch in system_a.system["node"][_nd]["output"]:
                _n.add_out_channel(_ch)

        """创建同步器"""
        if "synchronizer" in system_a.system["node"][_nd]:
            if system_a.system["node"][_nd]["synchronizer"]:
                _sync = synchronizer.Synchronizer()
                _n.add_synchronizer(_sync)

    """2)创建通道"""
    for _ch in system_a.system["channel"]:
        _c = channel.Channel(_ch)
        register.R.add_channel(_c)

    """3)运行系统"""
    node_link = register.R.get_node_list()
    while True:
        for _nd in node_link:
            node_link[_nd].run()

        if register.R.is_empty():
            time.sleep(0)


if __name__ == "__main__":

    main()

