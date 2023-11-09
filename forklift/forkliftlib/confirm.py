# -*- coding: utf-8 -*-
#
# @description      confirm (YES|NO) class for displaying messages to the user
#
# @author           Andrea Benini
# @date             2023-11-05
# @license          GNU Affero General Public License v3.0
# @see              Basic Confirm class based on curses for displaying yes/no messageboxes
#
import math
import curses

import forkliftlib


class Confirm(object):
    def __init__(self, message='', title=None, footer=None, width=None, height=None, x=None, y=None, colors=(curses.COLOR_WHITE, curses.COLOR_BLACK),
                 messageButtons=['OK', 'Cancel'], messageSelected=0, screen=None):
        self.__result = -1
        # Calculating: x, y, width, height, size
        if not width:
            width = 0
            for line in message.splitlines():
                if width < len(line):
                    width = len(line)
            width += 4
        if not height:
            height = message.count('\n')+1 + 3
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
        buttonsLen = 0
        for button in messageButtons:
            buttonsLen += len(button)+3
        
        winButtons = curses.newwin(1, buttonsLen-1, y+height-2, x+width-buttonsLen)
        winButtons.bkgd(curses.color_pair(widgetColor))
        # print(height, buttonsLen, 10, x+width-buttonsLen+10)
        while True:
            buttonSel = pos = 0
            for button in messageButtons:
                try:
                    if buttonSel == messageSelected:
                        mode = curses.color_pair(widgetColor)|curses.A_REVERSE
                    else:
                        mode = curses.color_pair(widgetColor)|curses.A_NORMAL
                    winButtons.addstr(0, pos, '<'+str(button)+'>', mode)
                except:     # Ignoring error on the last char
                    pass
                buttonSel += 1
                pos += len(button)+3
            winButtons.refresh()
            key = screen.getch()
            if key in [curses.KEY_ENTER, ord("\n")]:
                self.__result = messageSelected
                return
            elif key == curses.KEY_LEFT:
                messageSelected = messageSelected-1 if messageSelected>0 else len(messageButtons)-1
            elif key == curses.KEY_RIGHT:
                messageSelected = messageSelected+1 if messageSelected<len(messageButtons)-1 else 0

    @property
    def value(self):
        return self.__result
