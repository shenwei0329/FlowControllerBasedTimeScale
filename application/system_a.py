# -*- coding: UTF-8 -*-
#
#   A system for sample
#   ===================
#   耦合振荡器
#

import time
from event import event
import numpy
from displayer import displayer

CoX = 80
W0 = numpy.pi/15.
sin_W0 = numpy.sin(W0)
cos_W0 = numpy.cos(W0)
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
            Outer.printColorIdx("White", " ")
    print("")
    # print(_str)


def timer():
    return time.time()


def z_func(events, _):
    """
    一阶z函数
    :param events: 输入事件
    :param _:
    :return: 延迟事件
    """
    """延迟一个时标"""
    return event.Event(events[0].get_time_scale()+1, {"val": events[0].get_data()["val"]})


def init_event():
    return [event.Event(0, {"val": 1.})]


def sin_w0(val, sn):
    global sin_W0
    return event.Event(sn, {"val": val*sin_W0})


def cos_w0(val, sn):
    global cos_W0
    return event.Event(sn, {"val": val*cos_W0})


def sin_func(events, _):
    _data = events[0].get_data()
    return sin_w0(_data["val"], events[0].get_time_scale())


def minus_sin_func(events, _):
    _data = events[0].get_data()
    return sin_w0(-_data["val"], events[0].get_time_scale())


def cos_func(events, _):
    _data = events[0].get_data()
    return cos_w0(_data["val"], events[0].get_time_scale())


def sum_node(events, _):
    _data = {"val": 0.}
    for _e in events:
        if _e.get_status():
            _val = _e.get_data()
            _data["val"] += _val["val"]
    _e = event.Event(events[0].get_time_scale(), _data)
    return _e


def mix_node(events, _):
    _data = {"val": 1.}
    for _e in events:
        if _e.get_status():
            _val = _e.get_data()
            _data["val"] *= _val["val"]
    _e = event.Event(events[0].get_time_scale(), _data)
    return _e


def outer(_events, _):
    if len(_events) == 0:
        return None

    _v = []
    for _e in _events:
        __val = _e.get_data()
        if __val is not None:
            _v.append(int(__val['val']*15.))

    show(_v,
         [
             "*",
             "+",
             "x",
             "[",
             "]"
         ],
         [
             "White",
             "Yellow",
             "Red",
             "Red",
             "Red"
         ])
    return None


# 定义系统
# 耦合振荡器
#
system = {
    "node": {
        "z_node_1": {
            "input": [
                "C1",
            ],
            "output": [
                "C3",
                "C4"
            ],
            "function": z_func,
        },
        "z_node_2": {
            "input": [
                "C2",
            ],
            "output": [
                "C5",
                "C6"
            ],
            "function": z_func,
        },
        "cos_1": {
            "input": [
                "C3"
            ],
            "output": [
                "C7"
            ],
            "function": cos_func
        },
        "sin_1": {
            "input": [
                "C4"
            ],
            "output": [
                "C8"
            ],
            "function": sin_func
        },
        "cos_2": {
            "input": [
                "C6"
            ],
            "output": [
                "C10"
            ],
            "function": cos_func
        },
        "sin_2": {
            "input": [
                "C5"
            ],
            "output": [
                "C9"
            ],
            "function": minus_sin_func
        },
        "sum_1": {
            "input": [
                "C7",
                "C9",
            ],
            "output": [
                "C1",
                "C11",
                "C31"
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": sum_node,
            "init": init_event
        },
        "sum_2": {
            "input": [
                "C8",
                "C10",
            ],
            "output": [
                "C2",
                "C12",
                "C32"
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": sum_node,
            "init": init_event
        },
        "mix": {
            "input": [
                "C31",
                "C32"
            ],
            "output": [
                "C33"
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": mix_node,
        },
        "outer": {
            "input": [
                "C11",
                "C12",
                "C33"
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": outer
        }
    },
    "channel": [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "C12",
        "C31",
        "C32",
        "C33",
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

