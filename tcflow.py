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
from event import event
from register import register
from synchronizer import synchronizer

logging.basicConfig(filename="tcflow.log",
                    filemode="w",
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S",
                    encoding="utf-8",
                    level=logging.DEBUG)


def func1(_event):
    print(">>> func1")
    _data = {
        "val": 1,
    }
    return event.Event(_data)


def func11(events):
    print(">>> func11")
    _data = {"val": 0}
    for _e in events:
        _val = _e.get_data()
        _data["val"] = _val["val"] + 1
    _e = event.Event(_data)
    _e.set_time_scale(events[0].get_time_scale())
    return _e


def func12(events):
    print(">>> func12")
    _data = {"val": 0}
    for _e in events:
        _val = _e.get_data()
        _data["val"] = _val["val"] * 10
    _e = event.Event(_data)
    _e.set_time_scale(events[0].get_time_scale())
    return _e


def func2(_events):
    print(">>> func2")
    if len(_events) == 0:
        return None

    _val = 0
    for _e in _events:
        _val += _e.get_data()['val']
    print ">>> ", _val, " <<<"
    return None


# 定义系统
system = {
    "node": {
        "N1": {
            "output": [
                "C1.1",
                "C1.2",
            ],
            "function": func1
        },
        "nN1": {
            "input": [
                "C1.1",
            ],
            "output": [
                "C2.1",
            ],
            "function": func11
        },
        "nN2": {
            "input": [
                "C1.2",
            ],
            "output": [
                "C2.2",
            ],
            "function": func12
        },
        "N2": {
            "input": [
                "C2.1",
                "C2.2",
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": func2
        }
    },
    "channel": [
        "C1",
        "C1.1",
        "C1.2",
        "C2.1",
        "C2.2",
    ]
}


def main():

    logging.info("<%s> Starting" % __name__)

    # 创建注册器实体
    register.R = register.Register()

    """构建系统"""
    for _nd in system["node"]:
        # 创建节点
        print _nd
        _n = node.Node(_nd)
        _n.add_function(system["node"][_nd]["function"])
        register.R.add_node(_n)

        """创建输入通道"""
        if "input" in system["node"][_nd]:
            for _ch in system["node"][_nd]["input"]:
                _n.add_in_channel(_ch)

        """创建输出通道"""
        if "output" in system["node"][_nd]:
            for _ch in system["node"][_nd]["output"]:
                _n.add_out_channel(_ch)

        """创建同步器"""
        if "synchronizer" in system["node"][_nd]:
            if system["node"][_nd]["synchronizer"]:
                _sync = synchronizer.Synchronizer()
                _n.add_synchronizer(_sync)

    for _ch in system["channel"]:
        # 创建通道
        print _ch
        _c = channel.Channel(_ch)
        register.R.add_channel(_c)

    node_link = register.R.get_node_list()
    while True:
        for _nd in node_link:
            node_link[_nd].run()

        time.sleep(1)


if __name__ == "__main__":

    main()

