# -*- coding: UTF-8 -*-
#
#   A system for sample
#   ===================
#
#

import random
import time
from event import event

random.seed = time.time()

ts = 0


def func1(_event):
    global ts

    # print(">>> func1")
    _ts = int(time.time()*5)

    if ts == _ts:
        return None

    ts = _ts
    _data = {
        "val": random.random(),
    }
    return event.Event(_data)


def func11(events):
    print(">>> func11"),
    _data = {}
    for _e in events:
        _val = _e.get_data()
        print _val["val"],
        _data["val"] = _val["val"] + 1.13
    print _data["val"]
    _e = event.Event(_data)
    _e.set_time_scale(events[0].get_time_scale())
    return _e


def func12(events):
    print(">>> func12"),
    _data = {"val": 0}
    for _e in events:
        _val = _e.get_data()
        print _val["val"],
        _data["val"] = _val["val"] * 11.33
    print _data["val"]
    _e = event.Event(_data)
    _e.set_time_scale(events[0].get_time_scale())
    return _e


def func2(_events):
    print(">>> func2"),
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

