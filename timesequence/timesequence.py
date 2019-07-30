# -*- coding: UTF-8 -*-
#
#   The package for TimeSequence
#   ============================
#   时序
#
#   时序，是一个系统运行的时标基准，每一个系统必须定义它的唯一的时序。
#
#

import time


class TimeSequence:

    def __init__(self, time_policy=None):
        if time_policy is None:
            self.func = time.time
            self.ratio = 1
        else:
            self.func = time_policy["func"]
            self.ratio = time_policy["ratio"]
        self.sequence = 0
        self.old_ts = -1

    def set_ratio(self, ratio):
        if ratio >= 1:
            self.ratio = ratio

    def wait(self):
        while True:
            _ts = int(self.func() * self.ratio)
            if _ts != self.old_ts:
                self.old_ts = _ts
                self.sequence += 1
                return self.sequence-1
            time.sleep(0.01)

