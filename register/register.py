# -*- coding: UTF-8 -*-
#
#   The package for register
#


R = None


class Register:

    def __init__(self):
        self.node_link = {}
        self.channel_link = {}

    def add_node(self, node):
        self.node_link[node.get_name()] = node

    def add_channel(self, channel):
        self.channel_link[channel.get_name()] = channel

    def get_node(self, name):
        if name in self.node_link:
            return self.node_link[name]
        return None

    def get_channel(self, name):
        if name in self.channel_link:
            return self.channel_link[name]
        return None

    def get_node_list(self):
        return self.node_link

