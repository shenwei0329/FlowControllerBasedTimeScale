# -*- coding: UTF-8 -*-
#
#   A system for sample
#   ===================
#   Simulation of AM
#

import random
import time
from event import event
import numpy
from displayer import displayer

CoX = 80
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


def sin_func(_event, sn):
    # print(">>> func1")
    _data = {
        "val": 1.2 + 0.8*numpy.sin(2*numpy.pi*float(sn)/100.),
    }
    return event.Event(sn, _data)


def cos_func(_event, sn):
    # print(">>> func1")
    _data = {
        "val": 5.*numpy.cos(2*numpy.pi*float(sn)/10.),
    }
    return event.Event(sn, _data)


def noise(_event, sn):
    # print(">>> noise")
    _data = {
        "val": 1. + 0.2 * random.uniform(-1, 1),
    }
    return event.Event(sn, _data)


def multi_func(events, _):
    # (">>> func11"),
    _data = {"val": 1.0}
    for _e in events:
        if _e.get_status():
            _val = _e.get_data()
            # print _val["val"],
            _data["val"] *= _val["val"]
    # print _data["val"]
    _e = event.Event(events[0].get_time_scale(), _data)
    return _e


def func2(_events, _):
    # print(">>> func2"),
    if len(_events) == 0:
        return None

    _v = []
    for _e in _events:
        __val = _e.get_data()
        if __val is not None:
            _v.append(int(__val['val']*5.))

    show(_v,
         [
             "*",
             "+",
             "-",
             "x",
             "[",
             "]",
         ],
         [
             "White",
             "DarkSkyBlue",
             "DarkGreen",
             "DarkRed",
             "Red",
             "Red",
         ])
    return None


# 定义系统
# 三信号源的信号经过一个“乘法器”处理后输出到展示节点
#
system = {
    "node": {
        "sin": {
            "output": [
                "C1.1",
                "C2.3"
            ],
            "function": sin_func
        },
        "cos": {
            "output": [
                "C1.2",
                "C2.2"
            ],
            "function": cos_func
        },
        "noise": {
            "output": [
                "C1.3",
                "C2.4"
            ],
            "function": noise
        },
        "nN1": {
            "input": [
                "C1.1",
                "C1.2",
                "C1.3",
            ],
            "output": [
                "C2.1",
            ],
            # 定义一个同步器
            "synchronizer": True,
            "function": multi_func
        },
        "N2": {
            "input": [
                "C2.1",
                "C2.2",
                "C2.3",
                "C2.4"
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
        "C1.3",
        "C2.1",
        "C2.2",
        "C2.3",
        "C2.4"
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

