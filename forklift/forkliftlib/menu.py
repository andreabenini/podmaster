# -*- coding: utf-8 -*-
#
# @description      Menu class for bare user input
#
# @author           Andrea Benini
# @date             2023-11-07
# @license          GNU Affero General Public License v3.0
# @see              Basic inputbox for simple text editing, it's not even close to Zenith or a real editor
#
import curses

import forkliftlib


class Menu(object):
    def __init__(self, colors=(curses.COLOR_WHITE, curses.COLOR_BLACK), screen=None):
        self.__screen = screen
        del self.items
        self.__UUID = forkliftlib.UUID
        forkliftlib.UUID += 1
        curses.start_color()
        (colorForeground, colorBackground) = colors
        curses.init_pair(self.__UUID, colorForeground, colorBackground)

    @property
    def items(self):
        return self.__items
    @items.setter
    def items(self, value):
        self.__items = value
    @items.deleter
    def items(self):
        self.items = []
    def itemAdd(self, value):
        self.__items.append(value)

    
    def __displayGetElement(self, item):
        if type(item) == tuple or type(item)==list:
            return str(item[0])
        elif type(item) == dict:
            return next(iter(item.items()))
        return item
    
    def __displayItemsWidth(self):
        width = 0
        count = 0
        for i in self.__items:
            elementLength = len(self.__displayGetElement(i))
            if elementLength > width:
                width = elementLength
            count += 1
        return width

    def __displayItems(self, X, Y, lines, itemWidth, firstItem):
        # Detecting first item
        if firstItem > self.__selected:                         # scroll up management
            firstItem = self.__selected
        if firstItem+lines-1 < self.__selected:                 # scroll down management
            firstItem += 1
        # Display elements in a window
        winItems = curses.newwin(lines, itemWidth, Y, X)
        for key in range(0, lines):
            if firstItem+key < len(self.__items):               # Items to display
                value = self.__items[firstItem+key]
                element = self.__displayGetElement(value)
                element += (itemWidth-len(element))*' '
                element = element[:itemWidth]
                if firstItem+key == self.__selected:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                try: winItems.addstr(key, 0, element, curses.color_pair(self.__UUID)|mode)
                except curses.error: pass       # Writing a char in the last position causes an error, ignoring it
            else:
            # if firstItem+key+1 >= len(self.__items):
                try: winItems.addstr(key, 0, itemWidth*' ', curses.color_pair(self.__UUID))
                except curses.error: pass       # Writing a char in the last position causes an error, ignoring it
        # Refresh, return [firstItem], exit
        winItems.refresh()
        self.__screen.refresh()
        curses.doupdate()
        return firstItem

    def Display(self, X=0, Y=0, firstItem=0, caption=None, footer=None, lines=None, itemWidth=None, keys=[]):
        if len(self.__items) <= 0:
            return -1
        if not itemWidth:
            itemWidth = self.__displayItemsWidth()
        maxLines = curses.LINES - Y
        if not lines:
            lines = maxLines-2 if caption else maxLines
        # Menu Box, if any
        if caption:
            winBorder = curses.newwin(lines, itemWidth, Y, X)
            winBorder.bkgd(curses.color_pair(self.__UUID))
            winBorder.box()
            if caption and caption!="":
                winBorder.addstr(0, 1, f" {caption} ")
            if footer and footer!="":
                winBorder.addstr(lines-1, itemWidth-len(footer)-1, f"{footer}")
            winBorder.refresh()
            itemWidth -= 2
            lines -= 2
            X += 1
            Y += 1
        # Init vars
        X = 0 if X<0 else X
        Y = 0 if Y<0 else Y
        self.__selected = firstItem
        while True:
            # Display elements
            firstItem = self.__displayItems(X, Y, lines, itemWidth, firstItem)
            # Cursor movement
            key = self.__screen.getch()
            if key in [curses.KEY_ENTER, ord("\n")]:            # Item Selection
                return self.__selected
            elif key == 0x1B:                                   # Escape
                return -1
            elif key == curses.KEY_UP:                          # Cursor UP
                self.__navigate(-1)
            elif key == curses.KEY_DOWN:                        # Cursor DOWN
                self.__navigate(1)
            elif key == curses.KEY_HOME:                        # First item
                self.__selected = 0
            elif key == curses.KEY_END:                         # Last item
                self.__selected = len(self.__items) - 1
            elif key in keys:
                return (-2 - keys.index(key))

    def __navigate(self, n):
        self.__selected += n
        if self.__selected < 0:
            self.__selected = 0
        elif self.__selected >= len(self.__items) - 1:
            self.__selected = len(self.__items) - 1
