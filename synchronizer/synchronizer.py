# -*- coding: UTF-8 -*-
#
#   The package for Synchronizer
#   ============================
#   同步器
#
#

from event import event


class Synchronizer:

    def __init__(self):
        self.channels = []

    def add_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)

    def has_sync(self, rg):
        """
        判断指定的每个输入通道是否具有同一时标的事件。
        :param rg: 注册器
        :return:
        原则:
        1）若具有，则返回True；
        2）若不具有，且没有失步情况，则返回False；
        3）若失步，则补充一个异常事件并返回True。
        判断失步：当某一通道的事件时标不同于其它通道时，则该通道出现失步。
        """
        if len(self.channels) <= 1:
            return True

        _ts = []
        # print ">>> sync: ",
        for _qn in self.channels:
            _q = rg.get_channel(_qn)
            _e = _q.get_first()
            if _e is None:
                # print "no event"
                return False
            _ts.append({"q": _q, "ts": _e.get_time_scale()})

        _ts_min = sorted(_ts, key=lambda x: x["ts"])
        _ts_max = sorted(_ts, key=lambda x: x["ts"], reverse=True)
        if _ts_min[0]["ts"] == _ts_max[0]["ts"]:
            return True

        _ts = _ts_min[0]["ts"]
        for __ts in _ts_min[1:]:
            if __ts["ts"] == _ts:
                continue
            # print("...No sync!")
            """插入失步异常事件到队列"""
            _event = event.Event(None)
            _event.set_status(False)
            _event.set_time_scale(_ts)
            __ts["q"].insert_q(_event)

        return False


