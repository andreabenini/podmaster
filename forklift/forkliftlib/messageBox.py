# -*- coding: utf-8 -*-
#
# @description      MessageBox class for displaying messages to the user
#
# @author           Andrea Benini
# @date             2023-10-29
# @license          GNU Affero General Public License v3.0
# @see              Basic messageBox class based on curses for simple message output
#
import math
import curses

import forkliftlib


class MessageBox(object):
    def __init__(self, title=None, message='', footer=None, width=None, height=None, x=None, y=None, colors=(curses.COLOR_WHITE, curses.COLOR_BLACK), keypress=True):
        # Calculating: x, y, width, height, size
        if not width:
            width = 0
            for line in message.splitlines():
                if width < len(line):
                    width = len(line)
            width += 4
        if not height:
            height = message.count('\n')+1 + 2
        if not x:
            cols  = curses.COLS  - 4
            x = math.floor((cols-width)/2) + 2
        if not y:
            lines = curses.LINES - 2
            y = math.floor((lines-height)/2) + 1
        # Box color setup
        widgetColor = forkliftlib.UUID
        forkliftlib.UUID += 1
        (colorForeground, colorBackground) = colors
        curses.start_color()
        curses.init_pair(widgetColor, colorForeground, colorBackground)
        # Window border and title, if any
        winBorder = curses.newwin(height, width, y, x)
        winBorder.bkgd(curses.color_pair(widgetColor))
        winBorder.box()
        if title and title!="":
            winBorder.addstr(0, 1, f" {title} ")
        if footer and footer!="":
            xFooter = width-1-len(footer)
            if xFooter<=0:
                xFooter = 0
                footer = footer[:width-1]
            winBorder.addstr(height-1, xFooter, footer)
        winBorder.refresh()
        # Message box
        winMessage = curses.newwin(height-2, width-3, y+1, x+2)
        winMessage.bkgd(curses.color_pair(widgetColor))
        yline = 0
        for line in message.splitlines():
            try:
                winMessage.addstr(yline, 0, str(line), curses.color_pair(widgetColor))
            except curses.error: pass
            yline += 1
        winMessage.refresh()
        if keypress:
            winMessage.getch()
