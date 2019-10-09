# -*- coding: UTF-8 -*-
#
#   The package for bridge
#
#   利用Redis的发布与订阅方式，创建跨主机间事件传递的“桥”
#

import redis
import json


class Bridge:

    def __init__(self, config):
        self.__conn = redis.Redis(config['host'], config['port'])
        self.name = config['name']

    def public(self, msg):
        self.__conn.publish(self.name, json.dumps(msg))
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.name)
        pub.parse_response()
        return pub


def writer4test():
    channel = {'host': "10.111.30.195", 'port': "6379", 'name': "ch001"}
    obj = Bridge(channel)
    obj.public([{'item_id': '12315', 'type_id': 5, 'content': u'redis测试信息。'}])


def reader4test():
    channel = {'host': "10.111.30.195", 'port': "6379", 'name': "ch001"}
    obj = Bridge(channel)
    redis_sub = obj.subscribe()
    while True:
        msg = redis_sub.parse_response()
        if len(msg) == 3:
            print json.loads(msg[2])

