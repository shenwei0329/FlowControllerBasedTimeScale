# -*- coding: UTF-8 -*-
#
#   The package for node
#

import time
import logging


class Event:

    def __init__(self, sn, data):
        """
        构建一个事件实体
        :param sn: 时标
        :param data: 数据
        """
        self.time_scale = sn
        self.data = data
        """事件状态"""
        self.ok_status = True
        """事件寿命"""
        self.lifetime = None

        logging.info("%s: <%s>" % (__name__, str(self.time_scale)))

    def get_status(self):
        return self.ok_status

    def set_status(self, status):
        self.ok_status = status

    def get_time_scale(self):
        return self.time_scale

    def set_time_scale(self, sn):
        self.time_scale = sn

    def get_data(self):
        return self.data

    def update_data(self, data):
        self.data = data

