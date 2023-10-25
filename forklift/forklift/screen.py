import curses
import subprocess

import forklift

class Screen(object):
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)
        self.Clear()

    def close(self):
        curses.curs_set(1)
        curses.endwin()

    @property
    def screen(self):
        return self.__screen
    @screen.setter
    def screen(self, value):
        self.__screen = value

    def Clear(self):
        self.screen.clear()
        self.Refresh()

    def Refresh(self):
        self.screen.refresh()

    def Text(self, Caption='', X=0, Y=0, colorPair=None):
        if not colorPair:
            self.screen.addstr(Y, X, Caption)
        else:
            self.screen.addstr(Y, X, Caption, curses.color_pair(colorPair))

    def KeyPress(self):
        self.Refresh()
        return self.screen.getch()

    # Pause curses and execute command
    def Exec(self, command):
        curses.def_prog_mode()
        curses.endwin()
        subprocess.run(command, shell=True)
        curses.reset_prog_mode()
        self.Refresh()

    def newUUID(self):
        UUID = forklift.UUID
        forklift.UUID += 1
        return UUID
