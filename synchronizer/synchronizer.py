# -*- coding: UTF-8 -*-
#
#   The package for register
#
from register import register

class Synchronizer:

    def __init__(self):
        self.channels = []

    def add_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)

    def has_sync(self):
        if len(self.channels) <= 1:
            return True

        _ts = None
        for _qn in self.channels:
            _q = register.R.get_channel(_qn)
            _e = _q.get_first()
            if _e is None:
                return False
            __ts = _e.get_time_scale()
            if _ts is None:
                _ts = __ts
            else:
                if __ts != _ts:
                    return False

        return True

