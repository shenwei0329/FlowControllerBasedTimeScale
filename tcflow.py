# -*- coding: UTF-8 -*-
#
#   TCFlow
#   ======
#   A Flow Control system based on Time scale
#
#   基于时标的流控制系统体系
#   核心单元：节点Node、通道Channel和事件Event
#
#   事件是数据载体，它通过通道传递，由节点进行处理。
#   异常处理：
#   1）对于时标处理，若某个时标事件在处理时出现异常，则应该设置事件状态为异常，并继续它的流程。
#   2）若事件在传输过程中丢失，在其下游节点会发现通道事件失步，即接收到下一个时序事件，节点应该
#   补充一个异常事件并继续它的流程。
#   3）由节点决定对含有异常时标事件的处理。
#
#   2019-07-30：
#   如何考虑反馈机制，就时标而言，反馈事件是对应于当前被处理事件时标的下一个时标，就此应考虑采用
#   一个连续的整数序列为时标基。
#
#

import logging
from application import system_a
from application import system_b
from application import system_c
from application import system_d
from system import system
from displayer import displayer
import sys

logging.basicConfig(filename="tcflow.log",
                    filemode="w",
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S",
                    encoding="utf-8",
                    level=logging.ERROR)


def main():

    logging.info("<%s> Starting" % __name__)

    _sys = system.System(system_a.init_police)
    _displayer = displayer.Displayer()

    if len(sys.argv) > 1:
        if "a" in sys.argv[1]:
            _sys = system.System(system_a.init_police)
        elif "b" in sys.argv[1]:
            _sys = system.System(system_b.init_police)
        elif "c" in sys.argv[1]:
            _sys = system.System(system_c.init_police)
        elif "d" in sys.argv[1]:
            _sys = system.System(system_d.init_police)

    while True:
        _sys.run()


if __name__ == "__main__":

    main()

