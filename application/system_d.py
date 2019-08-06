# -*- coding: UTF-8 -*-
#
#   A system for sample
#   ================================
#   Simulation of Queue
#
#   假设：
#       1）负载按时间均衡规律达到，或
#       2）负载按正态分布达到
#
#

import time
from event import event
import random
from displayer import displayer
import numpy as np
import math

random.seed = time.time()
CoX = 80
# 服务率
miu = 7.5
# 到达率
lmd = 18
# 队列长度
L = 40
# 总负载量
Q = 0
MaxQ = 1200
# 等待量
q = 0
Ts = 0

Outer = displayer.Displayer()


def show(xs, formats, colors, tail=""):
    global CoX, Ts

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
    print(tail)
    # print(_str)


def timer():
    return time.time()


def normal(t, u=570., sig=34.641016):
    """
    正态分布
    :param t: 时序
    :param u: 数学期望值，取值 180
    :param sig: 方差，取值 5.4772255751
    :return: 期望值
    """
    return np.exp(-(math.pow(float(t)-u, 2) / (2. * math.pow(sig, 2)))) / (math.sqrt(2. * math.pi) * sig)


def launch_lamd_func(_event, sn):
    global Q, lmd
    if Q > lmd:
        _q = lmd * normal(sn)
        print _q
        _data = {
            "val": _q,
        }
        Q -= _q
    elif Q > 0:
        _data = {
            "val": Q,
        }
        Q = 0
    else:
        _data = {
            "val": 0,
        }
    return event.Event(sn, _data)


def launch_normal_func(_event, sn):
    global Q, MaxQ
    _q = MaxQ * normal(sn)
    Q += _q
    _data = {
        "val": _q,
    }
    return event.Event(sn, _data)


def outer(_events, sn):
    global Q, q, miu, CoX, MaxQ, L, Ts
    _data = _events[0].get_data()
    q += _data["val"]
    # _miu = miu * random.uniform(0.5, 1.2)
    _miu = miu
    if q >= _miu:
        q -= _miu
    else:
        q = 0

    if q < L:
        _color = ["White", "White", "Red", "Red"]
    else:
        _color = ["Yellow", "Red", "Red", "Red"]

    Ts = sn
    show([int(Q*(CoX-1)/MaxQ), int(q*(CoX-1)/MaxQ)],
         [
             "+",
             "x",
             "[",
             "]",
         ],
         _color,
         tail="%.1f" % (float(sn)/60.) + " " + "%.3f" % q + " " + "%.3f" % Q)
    return None


# 定义系统
#
system = {
    "node": {
        "launch": {
            "output": [
                "C1",
            ],
            "function": launch_normal_func
        },
        "outer": {
            "input": [
                "C1",
            ],
            "function": outer
        }
    },
    "channel": [
        "C1",
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
        "ratio": 10,
        "ts": 480,
    }
}

