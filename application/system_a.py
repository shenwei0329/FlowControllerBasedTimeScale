# -*- coding: UTF-8 -*-
#
#   A system for sample
#   ===================
#
#

import random
import time
from event import event
import numpy

random.seed = time.time()

sin_ts = 0
cos_ts = 0
noise_ts = 0


def sin_func(_event):
    global sin_ts

    # print(">>> func1")
    _ts = int(time.time()*10)

    if sin_ts == _ts:
        return None

    sin_ts = _ts
    _data = {
        "val": 6.*numpy.sin(2*numpy.pi*float(_ts)/73.3),
    }
    return event.Event(_data)


def cos_func(_event):
    global cos_ts

    # print(">>> func1")
    _ts = int(time.time()*10)

    if cos_ts == _ts:
        return None

    cos_ts = _ts
    _data = {
        "val": 3.* numpy.cos(2*numpy.pi*float(_ts)/9),
    }
    return event.Event(_data)


def noise(_event):
    global noise_ts

    # print(">>> noise")
    _ts = int(time.time()*10)

    if noise_ts == _ts:
        return None

    noise_ts = _ts
    _data = {
        "val": 0.333 * random.random(),
    }
    return event.Event(_data)


def multi_func(events):
    # (">>> func11"),
    _data = {"val": 0.0}
    for _e in events:
        _val = _e.get_data()
        # print _val["val"],
        _data["val"] += _val["val"]
    # print _data["val"]
    _e = event.Event(_data)
    _e.set_time_scale(events[0].get_time_scale())
    return _e


def show(ox, x, chr):
    _str = ""
    if x > ox:
        _str += " " * (ox-1)
        _str += "|"
        if (x-ox) > 1:
            _str += "-" * (x-ox-1)
        _str += chr
    elif x < ox:
        _str += " " * (x-1)
        _str += chr
        if (ox-x) > 1:
            _str += "-" * (ox-x-1)
        _str += "|"
    else:
        _str += " " * (ox-1)
        _str += chr
    _str += (' ' * (102 - len(_str)))
    _str += "%d" % (x - ox)
    print(_str)


def func2(_events):
    # print(">>> func2"),
    if len(_events) == 0:
        return None

    _val = 1.
    for _e in _events:
        # _val += _e.get_data()['val']
        _val *= _e.get_data()['val']
        _val = 51 + int(_val*5.)
    """
    for _n in range(51-int(_val*5.)):
        print " ",
    print "*"
    """
    show(51, _val, "*")
    return None


# 定义系统
# 三信号源的信号经过一个“乘法器”处理后输出到展示节点
#
system = {
    "node": {
        "sin": {
            "output": [
                "C1.1",
            ],
            "function": sin_func
        },
        "cos": {
            "output": [
                "C1.2",
            ],
            "function": cos_func
        },
        "noise": {
            "output": [
                "C1.3",
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
            ],
            "function": func2
        }
    },
    "channel": [
        "C1",
        "C1.1",
        "C1.2",
        "C1.3",
        "C2.1",
    ]
}

