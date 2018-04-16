'''Controls platform'''

import random as rd
import curses
import numpy as np
import random

class Board():
    '''The board for platform'''

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.noecho()
        curses.cbreak()
        curses.halfdelay(1)
        self.stdscr.keypad(True)
        self.board = np.zeros((10, 40))
        for j in range(40):
            if random.randint(0, 10) == 10:
                self.board[8][j] = 2
            self.board[9][j] = 1
        self.step = 0


        

    def output(self, string, pair=1):
        '''Outputs messages to the curses screen'''
        self.stdscr.addstr(string + '\n', curses.color_pair(pair))


    def disp(self):
        '''Displays the board and relevant instructions'''
        self.stdscr.clear()

        self.step += 1

        for i in range(10):
            for j in range(40):
                if self.board[i][(j + self.step) % 40] == 1:
                    self.stdscr.addstr('██', curses.color_pair(1))
                elif self.board[i][(j + self.step) % 40] == 2:
                    self.stdscr.addstr('◢◣', curses.color_pair(1))
                else:
                    self.stdscr.addstr('  ')
                    
            self.stdscr.addstr('\n')

        self.stdscr.refresh()
