# -*- coding: UTF-8 -*-
#
#   Displayer
#   =========
#   显示器
#
#   用于Windows系统字符终端显示
#

import ctypes
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x00
FOREGROUND_DARKBLUE = 0x01
FOREGROUND_DARKGREEN = 0x02
FOREGROUND_DARKSKYBLUE = 0x03
FOREGROUND_DARKRED = 0x04
FOREGROUND_DARKPINK = 0x05
FOREGROUND_DARKYELLOW = 0x06
FOREGROUND_DARKWHITE = 0x07
FOREGROUND_DARKGRAY = 0x08
FOREGROUND_BLUE = 0x09
FOREGROUND_GREEN = 0x0a
FOREGROUND_SKYBLUE = 0x0b
FOREGROUND_RED = 0x0c
FOREGROUND_PINK = 0x0d
FOREGROUND_YELLOW = 0x0e
FOREGROUND_WHITE = 0x0f

BACKGROUND_DARKBLUE = 0x10
BACKGROUND_DARKGREEN = 0x20
BACKGROUND_DARKSKYBLUE = 0x30
BACKGROUND_DARKRED = 0x40
BACKGROUND_DARKPINK = 0x50
BACKGROUND_DARKYELLOW = 0x60
BACKGROUND_DARKWHITE = 0x70
BACKGROUND_DARKGRAY = 0x80
BACKGROUND_BLUE = 0x90
BACKGROUND_GREEN = 0xa0
BACKGROUND_SKYBLUE = 0xb0
BACKGROUND_RED = 0xc0
BACKGROUND_PINK = 0xd0
BACKGROUND_YELLOW = 0xe0
BACKGROUND_WHITE = 0xf0


class Displayer:

    def __init__(self):
        self.handler = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        self.std_color = {
            "DarkBlue": FOREGROUND_DARKBLUE,
            "DarkGreen": FOREGROUND_DARKGREEN,
            "DarkSkyBlue": FOREGROUND_DARKSKYBLUE,
            "DarkRed": FOREGROUND_DARKRED,
            "DarkPink": FOREGROUND_DARKPINK,
            "DarkYellow": FOREGROUND_DARKYELLOW,
            "DarkWhite": FOREGROUND_DARKWHITE,
            "DarkGray": FOREGROUND_DARKGRAY,
            "Blue": FOREGROUND_BLUE,
            "Green": FOREGROUND_GREEN,
            "SkyBlue": FOREGROUND_SKYBLUE,
            "Red": FOREGROUND_RED,
            "Pink": FOREGROUND_PINK,
            "Yellow": FOREGROUND_YELLOW,
            "White": FOREGROUND_WHITE,
            "WhiteBlack": FOREGROUND_BLACK | BACKGROUND_WHITE,
            "YellowRed": BACKGROUND_YELLOW | FOREGROUND_RED,
        }

    def set_cmd_text_color(self, color):
        return ctypes.windll.kernel32.SetConsoleTextAttribute(self.handler, color)

    def resetColor(self):
        self.set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    def _print(self, color, mess):
        self.set_cmd_text_color(self.std_color[color])
        sys.stdout.write(mess)
        self.resetColor()

    def printColorIdx(self, idx, mess):
        if idx in self.std_color:
            self._print(idx, mess)
        else:
            self._print("YellowRed", mess)

