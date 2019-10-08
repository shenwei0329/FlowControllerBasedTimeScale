# -*- coding: UTF-8 -*-
#
#   A system for sample
#   ================================
#   Simulation of Digit Sin Generator
#

import time
from event import event
import numpy
from displayer import displayer

CoX = 80
W0 = numpy.pi/15.
sin_W0 = numpy.sin(W0)
cos_W0 = numpy.cos(W0)
A = 1.0
MAX = 0.
Outer = displayer.Displayer()


def show(xs, formats, colors):
    global CoX

    _str = " " * CoX * 2
    _str = _str[:CoX-1] + '|' + _str[CoX:]

    # print xs, formats

    for _xx in xs:
        _idx = xs.index(_xx)
        _x = CoX + _xx
        if _x > 0:
            if _x < (CoX*2 - 1):
                _str = _str[:_x-1] + formats[_idx] + _str[_x:]
            else:
                _str = _str[:-1] + "]"
        else:
            _str = "[" + _str[1:]

    for _s in _str:
        if _s != ' ':
            if _s == '|':
                Outer.printColorIdx("DarkWhite", _s)
            else:
                _idx = formats.index(_s)
                Outer.printColorIdx(colors[_idx], _s)
        else:
            Outer.printColorIdx("DarkBlue", " ")
    print("")
    # print(_str)


def timer():
    return time.time()


def q_func(_event, sn):
    global sin_W0, A
    """
    单位脉冲信号发生器
    :param _event: 
    :param sn: 
    :return: 
    """
    _data = {
        "val": A*sin_W0,
    }
    return event.Event(sn, _data)


def z_func(_event):
    """
    一阶z函数
    :param _event: 输入事件
    :return: 延迟事件
    """
    """延迟一个时标"""
    _event.set_time_scale(_event.get_time_scale()+1)
    return _event


def node_a(_events, _):
    _data = _events[0].get_data()
    _e = event.Event(z_func(_events[0]).get_time_scale(), _data)
    return _e


def init_node_a():
    return [event.Event(0, {"val": 0.})]


def node_b(_events, sn):
    _data = _events[0].get_data()
    _e = event.Event(z_func(_events[0]).get_time_scale(), {"val": -1.*_data["val"]})
    return _e


def init_node_b():
    return [
        event.Event(0, {"val": 0.}),
        event.Event(1, {"val": 0.}),
    ]


def node_c(_events, _):
    global cos_W0
    _data = _events[0].get_data()
    _e = event.Event(_events[0].get_time_scale(), {"val": _data["val"] * (2.0*cos_W0)})
    return _e


def sum_node(events, _):
    _data = {"val": 0.}
    for _e in events:
        if _e.get_status():
            _val = _e.get_data()
            _data["val"] += _val["val"]
    _e = event.Event(events[0].get_time_scale(), _data)
    return _e


def outer(_events, _):
    global MAX
    if len(_events) == 0:
        return None

    __val = _events[0].get_data()
    if __val is None:
        return None

    if MAX < __val["val"]:
        MAX = __val["val"]
    __val = int((__val["val"] - MAX*0.5)*5)
    show([__val],
         [
             "*",
             "[",
             "]",
         ],
         [
             "White",
             "Red",
             "Red",
         ])
    return None


# 定义系统
# 数字正弦波发生器
#
system = {
    "node": {
        "q": {
            "output": [
                "C0.1",
            ],
            "function": q_func
        },
        "node_a": {
            "input": [
                "C1.1",
            ],
            "output": [
                "C4.1",
                "C2.2",
            ],
            "function": node_a,
        },
        "node_b": {
            "input": [
                "C2.2",
            ],
            "output": [
                "C3.1",
            ],
            "function": node_b,
            "init": init_node_b
        },
        "node_c": {
            "input": [
                "C4.1",
            ],
            "output": [
                "C2.1",
            ],
            "function": node_c,
            "init": init_node_a
        },
        "sum_node": {
            "input": [
                "C0.1",
                "C2.1",
                "C3.1",
            ],
            "output": [
                "C1.1",
                "C1.2",
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": sum_node
        },
        "outer": {
            "input": [
                "C1.2",
            ],
            "function": outer
        }
    },
    "channel": [
        "C0.1",
        "C1.1",
        "C1.2",
        "C2.1",
        "C2.2",
        "C3.1",
        "C4.1",
    ]
}

""" 时标放大系数，基数是0.001秒
    因判断是取整后的值，所以ratio取值与时间片成反比
    ratio=100时，表述时间片为0.001*100取整，即10ms
    ratio=10时，表述时间片为0.001*10取整，即100ms
    ratio=1时，表述时间片为0.001*1取整，即1000ms（1秒）
"""
init_police = {
    "name": "system.a",
    "structure": system,
    "timer_police": {
        "func": timer,
        "ratio": 100,
    }
}

