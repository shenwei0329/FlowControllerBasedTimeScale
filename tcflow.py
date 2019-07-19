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

import time
import logging
from node import node
from channel import channel
from event import event

logging.basicConfig(filename="tcflow.log",
                    filemode="a",
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S",
                    encoding="utf-8",
                    level=logging.DEBUG)
node_link = []


def func1(_event):
    return event.Event("Here! %s" % time.time())


def main():

    logging.info("<%s> Starting" % __name__)
    # 创建输入根节点
    _nd = node.Node('root')
    _nd.add_function(func1)
    node_link.append(_nd)

    while True:
        for _nd in node_link:
            _nd.run()
            time.sleep(1)


if __name__ == "__main__":

    main()

