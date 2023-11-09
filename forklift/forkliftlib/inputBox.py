# -*- coding: utf-8 -*-
#
# @description      InputBox class for bare user input
#
# @author           Andrea Benini
# @date             2023-11-07
# @license          GNU Affero General Public License v3.0
# @see              Basic inputbox for simple text editing, it's not even close to Zenith or a real editor but it works
#
import math
import curses

# NOTE: Textbox curses class has a ~10Y bug:
#       - Submitted an issue here: https://github.com/python/cpython/issues/111795
#       - Provided a patch here:   https://github.com/python/cpython/pull/111796
# I'll wait them until it's merged in the main branch even if it might take years
# I'm now providing a modified (and working) version of it until then
# from   curses.textpad import Textbox      # Curses textpad object bug in standard library detected. USE THIS ONCE PATCHED
from   forkliftlib.textpad import Textbox      # This lib fixes the standard. REMOVE [textpad.py] WHEN FIXED IN THE CURSES LIB
import forkliftlib

class InputBox(object):
    def __init__(self, defaultValue="", title=None, footer=None, footer2=None, size=200, width=None, height=None, x=None, y=None, colors=(curses.COLOR_WHITE, curses.COLOR_BLACK)):
        # Calculating: x, y, width, height, size
        lines = curses.LINES - 2
        cols  = curses.COLS  - 4
        if not width:
            width = size if size<cols else cols
        if not height:
            if size<cols:
                height = 1
            else:
                height = size / width
                height = math.floor(height+1 if height%1 > 0 else height)
            height += 2
        if not x:
            x = math.floor((cols-width)/2) + 2
        if not y:
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
            if len(title) >= width+1:
                title = title[:width-4]
            winBorder.addstr(0, 1, f" {title} ")
        if footer and footer!="":
            if len(footer) >= width+1:
                footer = footer[:width-2]
            winBorder.addstr(height-1, width-1-len(footer), footer)
        if footer2 and footer2!="":
            if len(footer2) >= width+1:
                footer2 = footer2[:width-2]
            winBorder.addstr(height-1, 1, footer2)
        winBorder.refresh()
        # Edit field box
        curses.curs_set(1)
        winInput = curses.newwin(height-2, width-2, y+1, x+1)
        winInput.bkgd(curses.color_pair(widgetColor))
        winInput.addstr(str(defaultValue))
        winTextbox = Textbox(winInput, insert_mode=True)
        self.__result = ""
        winTextbox.edit(self.__SpecialCharsHandling)
        if self.__result is not None:
            self.__result = winTextbox.gather().strip()
            self.__result = self.__result[:size]
        curses.curs_set(0)

    def __SpecialCharsHandling(self, character):        # Special chars (home/end/ctrl/...) might be handled here
        if character == 10:                             # <CR>   -> Ctrl-G   (wtf, Ctrl+G to close the input ?)
            return 7
        elif character == 0x1B:                         # <Esc>  -> Abort. Ctrl-G + (None value)
            self.__result = None
            return 7
        elif character == 262:                          # <Home> -> Ctrl-A
            return 1
        elif character == 360:                          # <End>  -> Ctrl-E
            return 5
        elif character == 330:                          # <Canc> -> Ctrl-D
            return 4
        return character

    @property
    def value(self):
        return self.__result
