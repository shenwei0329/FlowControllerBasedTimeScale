# -*- coding: UTF-8 -*-
#
#   TCFlow
#   ======
#   A Flow Control system based on Time scale
#
#   基于时标的流控制系统体系
#   核心单元：节点Node、通道Channel
#
#

from node import node
from channel import channel


node_link = []


def main():

    # 创建输入根通道和根节点
    _nd = node.Node()
    _nd.add_out_channel(channel.Channel())
    node_link.append(_nd)

    while True:
        for _nd in node_link:
            _nd.run()


if __name__ == "__main__":

    main()

