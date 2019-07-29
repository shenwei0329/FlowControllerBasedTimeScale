# -*- coding: UTF-8 -*-
#
#   TCFlow
#   ======
#   A Flow Control system based on Time scale
#
#   基于时标的流控制系统体系
#   核心单元：节点Node、通道Channel和事件Event
#
#   事件是数据载体，它通过通道传递，由节点进行处理。
#   异常处理：
#   1）对于时标处理，若某个时标事件在处理时出现异常，则应该设置事件状态为异常，并继续它的流程。
#   2）若事件在传输过程中丢失，在其下游节点会发现通道事件失步，即接收到下一个时序事件，节点应该
#   补充一个异常事件并继续它的流程。
#   3）由节点决定对含有异常时标事件的处理。
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
                    level=logging.ERROR)


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

