# -*- coding: UTF-8 -*-
#
#   The package for node
#

import time
import logging


class Event:

    def __init__(self, data):
        self.time_scale = int(time.time())
        self.data = data
        self.ok_status = True
        self.lifetime = None

        logging.info("%s: <%s>" % (__name__, str(self.time_scale)))

    def get_time_scale(self):
        return self.time_scale

    def set_time_scale(self, ts):
        self.time_scale = ts

    def get_data(self):
        return self.data

    def update_data(self, data):
        self.data = data

