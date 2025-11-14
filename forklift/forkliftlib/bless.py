# -*- coding: utf-8 -*-
#
# @project      Bless: your favorite CLI/GUI library for quick applications
# @author       Andrea Benini
# @date         2023-11-07
# @license      GNU Affero General Public License v3.0
# @version      1.0
#
# @description  Have you had enough of fighting against curses ? Bless is the answer.
#               For simple application, few basic widgets and small interfaces curses
#               (or ncurses) is a big boilerplate and quite complex, it requires extra
#               code and costs you an extra dependency.
#               For quick standalone and dependencies free applications this is the best
#               way of providing some CLI/GUI capabilities written in pure python only.
#               There's no need of a virtual environment for it.
#
# pyright: reportMissingImports=false
# pyright: reportUndefinedVariable=false

# Python imports
import os
import sys
import tty
import math
import shutil
import termios


# Colors
BLACK           = (30,  00)
RED             = (31,  41)
GREEN           = (32,  42)
YELLOW          = (33,  43)
BLUE            = (34,  44)
MAGENTA         = (35,  45)
CYAN            = (36,  46)
WHITE           = (97, 107)
GREY_LIGHT      = (37,  47)
GREY_DARK       = (90,  40)

# Keys
KEY = {
    "ENTER":        '\r',
    "TAB":          '\t',
    "ESCAPE":       '\x1b',
    "BACKSPACE":    '\x7f',
    "F1":           '\x1bOP',
    "F2":           '\x1bOQ',
    "F3":           '\x1bOR',
    "F4":           '\x1bOS',
    "F5":           '\x1b[15~',
    "F6":           '\x1b[17~',
    "F7":           '\x1b[18~',
    "F8":           '\x1b[19~',
    "F9":           '\x1b[20~',
    "F10":          '\x1b[21~',
    "F12":          '\x1b[24~',
    "UP":           '\x1b[A',
    "DOWN":         '\x1b[B',
    "RIGHT":        '\x1b[C',
    "LEFT":         '\x1b[D',
    "HOME":         '\x1b[H',
    "END":          '\x1b[F',
    "INS":          '\x1b[2~',
    "DEL":          '\x1b[3~',
    "PAGE_UP":      '\x1b[5~',
    "PAGE_DOWN":    '\x1b[6~',
}
KEY_REMAP = {       # KEY set remapping for specific terminals
    "screen-256color": {    # tmux, screen-256color
        "HOME":         '\x1b[1~',      
        "END":          '\x1b[4~',
    }
}
def KEYname(key=None):
    for item in KEY:
        if KEY[item] == key:
            return item
    return None


class bless():
    def __init__(self, init=False):
        self.__cursor = True
        self.__screenGetInfo()
        self.__screenKeyRemap()
        self.color(Foreground=WHITE, Background=BLACK)
        if init:
            self.init()

    # Getting screen information
    def __screenGetInfo(self):
        terminal = shutil.get_terminal_size()
        self.__posX = self.__posY = 1
        self.__X    = terminal.columns
        self.__Y    = terminal.lines
        self.__term = os.environ.get("TERM")
    # Remap keys when dealing with different $TERM terminals
    def __screenKeyRemap(self):
        for term in KEY_REMAP:
            if term == self.__term:
                for key in KEY_REMAP[term]:
                    KEY[key] = KEY_REMAP[term][key]

    # Init screen
    def init(self, clear=True):
        if clear:
            self.clear()
        self.cursorHide()
    def clear(self, cursorHide=False):        # Clear screen and cursor at [1:1]
        if cursorHide:
            self.cursorHide()
        print("\033[2J\033[H", end='')
    # Close screen
    def close(self):
        if not self.cursorVisible():
            self.clear()
            self.cursorShow()
    # Class context manager (destructor-like method)
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def refresh(self):
        print("", end="", flush=True)

    # Pause/Restore system for external program exec()
    def pause(self):
        self.__cursorPause = self.cursorVisible()
        self.clear()
        self.cursorShow()
        self.refresh()
    def restore(self):
        self.clear()
        if not self.__cursorPause:
            self.cursorHide()
        self.refresh()

    # General properties
    @property           # Current X cursor position
    def X(self):
        return self.__posX
    @property           # Current Y cursor position
    def Y(self):
        return self.__posY
    @property           # Number of columns in the screen
    def cols(self):
        return self.__X
    @property           # Number of rows in the screen
    def rows(self):
        return self.__Y

    #...press any key to continue...
    def keyPress(self):
        self.keyGet()
    # keyGetSimple() Get a key from stdin, ANSI escape sequences are not properly detected, use keyGet() instead
    # @return (int) Pressed key, special keys are handled
    def keyGetSimple(self):
        oldSettings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            while True:
                b = os.read(sys.stdin.fileno(), 3).decode()
                if len(b) == 3:
                    k = ord(b[2])
                else:
                    k = ord(b)
                return k
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldSettings)
    
    # keyGet() Get key from stdin. Ordinary keys, F-Keys, Esc, cursor keys are fully tested and supported
    # @see Special keys detection method, raw stream input, works on all *nix systems, don't care about win
    def keyGet(self):
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            key = None
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if key == '\x1b':           # <esc> key or escape sequence
                os.set_blocking(fd, False)
                extraKey = sys.stdin.read(2)
                isNumber = False
                if len(extraKey) >= 2:
                    key += extraKey
                    isNumber = True if ord(extraKey[1]) >= 48 and ord(extraKey[1]) <= 57 else False     # \x1b[`1`..`9`
                if isNumber:
                    loopMax = 5         # Avoid possible loops or weird sequences without trailing '~'
                    while extraKey != '~' and loopMax > 0:
                        extraKey = sys.stdin.read(1)
                        loopMax -= 1
                        key += extraKey
            return key
        finally:
            os.set_blocking(fd, True)
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

    def cursorHide(self):
        self.__cursor = False
        print("\033[?25l", end='')
    def cursorShow(self):
        self.__cursor = True
        print("\033[?25h", end='')
    def cursorVisible(self):
        return self.__cursor
    def cursorMove(self, X=1, Y=1):
        if not X or not Y or X>self.cols or Y>self.rows:
            return
        print(f"\033[{Y};{X}H", end='', flush=True)

    # @param Foreground (tuple) (foreground(),background()) Colors expressed in a tuple, 2nd param will be ignored
    # @param Background (tuple|None) Background color (from the above table)
    def color(self, Foreground=None, Background=None):
        if not type(Foreground) is tuple:
            return
        if not type(Background) is tuple:
            (colorForeground, colorBackground) = (Foreground, Background)
            self.__colorForeground  = colorForeground[0]
            self.__colorForeground2 = colorForeground[1]
            self.__colorBackground  = colorBackground[1]
            self.__colorBackground2 = colorBackground[0]
        else:
            self.__colorForeground  = Foreground[0]
            self.__colorForeground2 = Foreground[1]
            self.__colorBackground  = Background[1]
            self.__colorBackground2 = Background[0]

    # @return (foreground,background) (tuple) Color codes based on bless colors definitions
    def colorGet(self, Color=None):
        if Color:   # User colors
            if type(Color[0]) is tuple and type(Color[1]) is tuple:     # Expressed as Color(Foreground(FOREGROUND,_), Background(_,BACKGROUND))
                return (Color[0][0], Color[1][1])
            return (Color[0], Color[1])
        return (self.__colorForeground, self.__colorBackground)         # No colors, picking defaults
    # Get REVERSED colors from [Color] or defaults colors (self.__*2)
    # @return (foreground,background) (tuple) Color codes based on bless colors definitions
    def colorGetReversed(self, Color=None):
        if Color:   # User colors
            if type(Color[0]) is tuple and type(Color[1]) is tuple:     # Expressed as Color(Foreground(FOREGROUND,_), Background(_,BACKGROUND))
                return (Color[1][0], Color[0][1])
            return (Color[1], Color[0])
        return (self.__colorBackground2, self.__colorForeground2)       # No colors, picking defaults

    # text() Print a string on screen
    # @param Text  (string) String to print
    # @param X     (int)    Text X/Col position (starting from 1)
    # @param Y     (int)    Text Y/Row position (starting from 1)
    # @param Text  (string) Text to write
    # @param Color (tuple)  (Foreground|Background) color for the text
    #              (tuple,tuple) -> (Foreground(FOREGROUND,_), Background(_,BACKGROUND))  [example: (bless.WHITE, bless.BLUE)]
    #              (None)   Defaults colors to (self.__colorForeground, self.__colorBackground)
    def text(self, Text='', X=1, Y=1, Color=None):
        Color = self.colorGet(Color=Color)
        if X>self.cols or Y>self.rows:
            return
        if X+len(Text) > self.cols+1:
            Text = Text[0 : self.cols-X-len(Text)+1]
        print(f"\033[{Y};{X}H\033[{Color[0]};{Color[1]}m{Text}\033[0m", end='', flush=True)

    # Return a multiline string from a oneliner, word splitting
    def textWrap(self, Text='', Max=0):
        if len(Text) <= Max:
            return Text
        Output = ''
        lineLen = 0
        for word in Text.split():
            if lineLen+len(word) > Max and lineLen != 0:
                Output += f'\n'
                lineLen = 0
            Output += f'{word} '
            lineLen += len(word)
        return Output

    # Get Max colum size from a multiline string
    def textGetColMax(self, Text=''):
        result = 0
        for line in Text.splitlines():
            if len(line) > result:
                result = len(line)
        return result

    # Center a [Text] in a string of length [Size]
    def textCenter(self, Text='', Size=None):
        Padding = 0 if not Size else Size-len(Text)
        if Padding < 0:
            Padding = 0
        PadLeft  = Padding // 2
        PadRight = Padding - PadLeft
        return ' '*PadLeft + Text[:Size] + ' '*PadRight

    # Just like a text() but inside a (possible colored) label
    def label(self, Text='', Size=None, X=1, Y=1, Color=None, Center=False, Line=False):
        Padding = 0 if not Size else Size-len(Text)
        if Line:
            Padding = self.cols-len(Text)
        if Padding < 0:
            Padding = 0
        if Center:
            PadLeft  = Padding // 2
            PadRight = Padding - PadLeft
        else:
            PadLeft  = 0
            PadRight = Padding
        self.text(Text=' '*PadLeft + Text + ' '*PadRight, X=X, Y=Y, Color=Color)

    # Draw a simpe box in the screen
    # @see Called by self.box() only
    def __box(self, X=1, Y=1, Width=1, Height=1, Color=None):
        self.text(Text="┌"+("─"*(Width-2))+"┐", X=X, Y=Y, Color=Color)          # Header
        for i in range(1, Height-1):
            self.text(Text="│"+" "*(Width-2)+"│", X=X, Y=Y+i, Color=Color)      # Body
        self.text(Text="└"+"─"*(Width-2)+"┘", X=X, Y=Y+Height-1, Color=Color)   # Footer

    # Add Title and Footer to a box
    # @see Called by self.box() only
    def __boxTitleFooter(self, Title=None, Footer=None, X=1, Y=1, Width=1, Height=1, Color=None):
        if Title and Title!="":
            if len(Title)>Width-4:
                Title = Title[:Width-4]
            self.text(Text=f" {Title} ", X=X+1, Y=Y, Color=Color)
        if Footer and Footer!="":
            xFooter = Width-1-len(Footer)
            if xFooter<=0:
                xFooter = 1
                Footer = Footer[:Width-2]
            self.text(Text=Footer, X=X+xFooter, Y=Y+Height-1, Color=Color)

    def box(self, Title=None, Footer=None, X=1, Y=1, Width=0, Height=0, Color=None):
        if Width < 2:
            Width = 2
        self.__box(X=X, Y=Y, Width=Width, Height=Height, Color=Color)
        self.__boxTitleFooter(Title=Title, Footer=Footer, X=X, Y=Y, Width=Width, Height=Height, Color=Color)

    def __boxMessage(self, Message=None, X=1, Y=1, Color=None):
        for line in Message.splitlines():
            self.text(Text=str(line), Y=Y, X=X, Color=Color)
            Y += 1

    def messageBox(self, Title=None, Message='', Footer=None, Width=None, Height=None, X=None, Y=None, Color=None, Keypress=True):
        if Color:
            Color = (Color[0][0], Color[1][1])
        else:
            Color = (self.__colorForeground, self.__colorBackground)
        # Calculating: x, y, width, height, size
        if not Width:
            Width = 0
            for line in Message.splitlines():
                if Width < len(line):
                    Width = len(line)
            Width += 4
        if not Height:
            Height = Message.count('\n')+1 + 2
        if not X:
            X = math.floor((self.cols-Width)/2) + 2
        if not Y:
            Y = math.floor((self.rows-Height)/2) + 1
        # Draw the box, title, footer, message
        self.box(Title=Title, Footer=Footer, X=X, Y=Y, Width=Width, Height=Height, Color=Color)
        self.__boxMessage(Message=Message, X=X+2, Y=Y+1, Color=Color)
        if Keypress:
            self.keyPress()

    # @return (int) Selected button, starting from 0
    def confirmBox(self, Title=None, Message='', Footer=None, Width=None, Height=None, X=None, Y=None, Color=None, MessageButtons=['OK', 'Cancel'], ButtonSelected=0):
        # Button Width
        buttonsWidth = 0
        for Button in MessageButtons:
            buttonsWidth += len(Button)+3
        # Calculating: x, y, width, height, size
        if not Width:
            Width = 0
            for line in Message.splitlines():
                if Width < len(line):
                    Width = len(line)
            if Width < buttonsWidth:
                Width = buttonsWidth
            Width += 4
        if not Height:
            Height = Message.count('\n')+1 + 3
        if not X:
            X = math.floor((self.cols-Width)/2) + 2
        if not Y:
            Y = math.floor((self.rows-Height)/2) + 1
        # Draw the box, title, footer, message
        self.box(Title=Title, Footer=Footer, X=X, Y=Y, Width=Width, Height=Height, Color=Color)
        self.__boxMessage(Message=Message, X=X+2, Y=Y+1, Color=Color)
        # Buttons
        while True:
            ButtonCurrent = pos = 0
            for Button in MessageButtons:
                if ButtonCurrent == ButtonSelected:
                    btnColor = self.colorGetReversed(Color=Color)
                else:
                    btnColor = self.colorGet(Color=Color)
                self.text(Text='<'+str(Button)+'>', X=X+Width-buttonsWidth+pos, Y=Y+Height-2, Color=btnColor)
                ButtonCurrent += 1
                pos += len(Button)+3
            key = self.keyGet()
            if key == KEY['ENTER']:
                return ButtonSelected
            elif key == KEY['LEFT']:
                ButtonSelected = ButtonSelected-1 if ButtonSelected>0 else len(MessageButtons)-1
            elif key == KEY['RIGHT']:
                ButtonSelected = ButtonSelected+1 if ButtonSelected<len(MessageButtons)-1 else 0

    def editBox(self, Title=None, Footer=None, Footer2=None, DefaultValue='', Size=100, Width=None, Height=None, X=None, Y=None, Color=None):
        if not Color:
            Color = ((self.__colorForeground, self.__colorForeground2), (self.__colorBackground2, self.__colorBackground))
        return _editBox(screen=self, Title=Title, Footer=Footer, Footer2=Footer2, DefaultValue=DefaultValue, Size=Size, Width=Width, Height=Height, X=X, Y=Y, Color=Color)

    def menu(self, Color=None, Items=None):
        if not Color:
            Color = ((self.__colorForeground, self.__colorForeground2), (self.__colorBackground2, self.__colorBackground))
        return _menu(screen=self, Color=Color, Items=Items)


# @see Do NOT use this class directly, use bless.menu() method as a wrapper instead
class _menu():
    def __init__(self, screen=None, Color=None, Items=[]):
        if not screen:
            return None
        self.__screen   = screen
        self.__Colors   = Color
        self.__selected = 0
        del self.items
        if Items:
            self.items  = Items

    @property
    def items(self):
        return self.__items
    @items.setter
    def items(self, value):
        self.__items = value
    @items.deleter
    def items(self):
        self.__items = []
    def itemAdd(self, value):
        self.__items.append(value)

    def __element(self, item):
        if type(item) == tuple or type(item)==list:
            return str(item[0])
        elif type(item) == dict:
            return next(iter(item.items()))
        return item

    def __itemsCalculate(self):
        width = 0
        items = 0
        for i in self.__items:
            elementLength = len(self.__element(i))
            if elementLength > width:
                width = elementLength
            items += 1
        return (items, width)

    def __displayItems(self, X, Y, Lines, ItemWidth, FirstItem):
        # Detecting first item
        if FirstItem > self.__selected:                         # scroll up management
            FirstItem = self.__selected
        if FirstItem+Lines-1 < self.__selected:                 # scroll down management
            FirstItem += 1
        # Display elements in a window
        for key in range(0, Lines):
            color = self.__screen.colorGet(Color=self.__Colors)
            if FirstItem+key < len(self.__items):               # Items to display
                value = self.__items[FirstItem+key]
                element = self.__element(value)
                element += (ItemWidth-len(element))*' '
                element = element[:ItemWidth]
                if FirstItem+key == self.__selected:
                    color = self.__screen.colorGetReversed(Color=self.__Colors)
                self.__screen.text(Text=element, X=X, Y=Y+key, Color=color)
            else:
                self.__screen.text(Text=ItemWidth*' ', X=X, Y=Y+key, Color=color)
        return FirstItem

    def __navigate(self, n):
        self.__selected += n
        if self.__selected < 0:
            self.__selected = 0
        elif self.__selected >= len(self.__items) - 1:
            self.__selected = len(self.__items) - 1

    # Display() Show the menu
    def Display(self, X=1, Y=1, FirstItem=0, Caption=None, Footer=None, Lines=None, ItemWidth=None, Keys=[]):
        if not self.__items or len(self.__items) == 0:
            return -1
        (itemsNumber, itemsMaxWidth) = self.__itemsCalculate()
        if not ItemWidth:
            ItemWidth = itemsMaxWidth+2 if Caption else itemsMaxWidth
        if Lines:
            if Lines > self.__screen.rows - Y:
                Lines = self.__screen.rows - Y
        else:
            if Caption:
                itemsNumber += 2
            if itemsNumber > self.__screen.rows - Y:
                Lines = self.__screen.rows - Y
            else:
                Lines = itemsNumber
        # Menu Box, if any
        if Caption:
            self.__screen.box(Title=Caption, Footer=Footer, X=X, Y=Y, Width=ItemWidth, Height=Lines, Color=self.__Colors)
            ItemWidth -= 2
            Lines -= 2
            X += 1
            Y += 1
        # Init vars
        X = 0 if X<0 else X
        Y = 0 if Y<0 else Y
        self.__selected = FirstItem
        while True:
            # Display elements
            FirstItem = self.__displayItems(X, Y, Lines, ItemWidth, FirstItem)
            # Cursor movement
            key = self.__screen.keyGet()
            if key == KEY['ENTER']:                             # Item Selection
                return self.__selected
            elif key == KEY['ESCAPE']:                          # Escape
                return -1
            elif key == KEY['UP']:                              # Cursor UP
                self.__navigate(-1)
            elif key == KEY['DOWN']:                            # Cursor DOWN
                self.__navigate(1)
            elif key == KEY['HOME']:                            # First item
                self.__selected = 0
            elif key == KEY['END']:                             # Last item
                self.__selected = len(self.__items) - 1
                FirstItem = self.__selected - Lines
                if FirstItem < 0:
                    FirstItem = 0
            elif KEYname(key=key) in Keys:
                return (-2 - Keys.index(KEYname(key)))

class _editBox():
    def __init__(self, screen=None, Title=None, Footer=None, Footer2=None, DefaultValue='', Size=100, Width=None, Height=None, X=1, Y=1, Color=None):
        self.__screen = screen
        self.__value  = str(DefaultValue)[:Size]
        # Calculating: x, y, width, height, size
        Size = int(Size) if Size else 100
        if not Width:
            Width = Size+4 if Size+4<self.__screen.cols else self.__screen.cols
        if not Height:
            Height = 2+((Size+4) // Width)+(1 if Size%Width>0 else 0)
        if not X:
            X = (self.__screen.cols-Width)  // 2 + 1
        if not Y:
            Y = (self.__screen.rows-Height) // 2 + 1
        # Box color setup
        self.__screen.box(Title=Title, Footer=Footer, X=X, Y=Y, Width=Width, Height=Height, Color=Color)
        if Footer2:
            self.__screen.text(X=X+1, Y=Y+Height-1, Color=Color, Text=str(Footer2[:Width-2]))
        # Edit field box
        self.__XStart = X+1
        self.__YStart = Y+1
        self.__Width  = Width-2
        self.__Height = Height-2
        self.__Colors = Color
        cursorVisible = self.__screen.cursorVisible()
        cursorPos     = len(self.__value)
        (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos)
        self.__fieldPrint(X=self.__XStart, Y=self.__YStart, Text=self.__value)
        self.__screen.cursorShow()
        self.__screen.cursorMove(X=xCursor, Y=yCursor)
        while True:
            key = self.__screen.keyGet()
            if key == KEY['ESCAPE']:                # Escape. abort and close the textfield
                self.__value = None
                key = KEY['ENTER']
            if key == KEY['ENTER']:                 # Enter. close the textfield
                if not cursorVisible:
                    self.__screen.cursorHide()
                return
            elif key == KEY['BACKSPACE']:           # Backspace
                if cursorPos > 0:
                    self.__value = self.__value[:cursorPos-1] + self.__value[cursorPos:]
                    cursorPos -= 1
                    (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos)
                    self.__fieldPrint(X=xCursor, Y=yCursor, Text=self.__value[cursorPos:])
            elif key == KEY['DEL']:
                if cursorPos < len(self.__value):
                    (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos)
                    self.__value = self.__value[:cursorPos] + self.__value[cursorPos+1:]
                    self.__fieldPrint(X=xCursor, Y=yCursor, Text=self.__value[cursorPos:])
            elif key == KEY['LEFT']:                # Left Arrow
                if cursorPos > 0:
                    cursorPos -= 1
                    (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos, clear=False)
            elif key == KEY['RIGHT']:               # Right Arrow
                if cursorPos < len(self.__value):
                    cursorPos += 1
                    (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos, clear=False)
            elif key == KEY['HOME']:                # Home
                cursorPos = 0
                (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos, clear=False)
            elif key == KEY['END']:                 # End
                cursorPos = len(self.__value)
                (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos, clear=False)
            else:                                   # Any key
                if len(self.__value) < Size:
                    self.__value = self.__value[:cursorPos] + key + self.__value[cursorPos:]
                    self.__fieldPrint(X=xCursor, Y=yCursor, Text=self.__value[cursorPos:])
                    cursorPos += 1
                    (xCursor, yCursor) = self.__fieldMove(posCursor=cursorPos, clear=False)
            self.__screen.cursorMove(X=xCursor, Y=yCursor)

    # Print [Text] in the editBox, starting from X/Y position
    def __fieldPrint(self, X=1, Y=1, Text=''):
        # Splitting string in two: [FirstPart],[Text] if it doesn't fits in the line
        StringPart = (X+len(Text)) - (self.__XStart+self.__Width)
        if StringPart > 0:
            FirstPart = Text[:-StringPart]
            self.__screen.text(X=X, Y=Y, Color=self.__Colors, Text=FirstPart)
            Text = Text[-StringPart:]
            X = self.__XStart
            if Y+1 > self.__YStart+self.__Height:
                return
            self.__fieldPrint(X, Y+1, Text=Text)
            return 
        self.__screen.text(X=X, Y=Y, Color=self.__Colors, Text=Text)
        return

    # Calculate [posCursor] inside the field and cleanup the field from it if it's necessary
    # @return (X,Y) (tuple) Current X/Y cursor position according to [posCursor] (calculated from field)
    def __fieldMove(self, posCursor=0, clear=True):
        xCursor = yCursor = None
        for i in range(0, self.__Height):
            if xCursor and yCursor and clear:
                self.__screen.text(Text=" "*self.__Width, X=self.__XStart, Y=self.__YStart+i, Color=self.__Colors)
            if not xCursor and posCursor < i*self.__Width + self.__Width:
                yCursor = self.__YStart+i
                xCursor = self.__XStart+(posCursor - i*self.__Width)
                if clear:
                    self.__screen.text(Text=" "*(self.__Width-xCursor+self.__XStart), X=xCursor, Y=yCursor, Color=self.__Colors)
        return (xCursor, yCursor)
    
    # Current value of the edit field
    @property
    def value(self):
        return self.__value
