'''Controls the Hunt board'''

import curses
import numpy as np
import random

class Board():
    '''The board for Hunt'''

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.board = np.zeros((15, 15), dtype=int)

        self.posy = random.randint(0, 14)
        self.posx = random.randint(0, 14)
        while 3 < self.posy < 11 or 3 < self.posx < 11:
            self.posy = random.randint(0, 14)
            self.posx = random.randint(0, 14)
        
        self.clear_fog()

        self.bearx = 7
        self.beary = 7
        self.traps = 5
        self.moves = 25
        self.can_clear_trees = 2

    def clear_fog(self):
        '''Clear the fog around the current position'''
        if self.posx == 0:
            x_small = 0
        else:
            x_small = self.posx - 1
        if self.posy == 0:
            y_small = 0
        else:
            y_small = self.posy - 1
        if self.posx == 14:
            x_big = 14
        else:
            x_big = self.posx + 1
        if self.posy == 14:
            y_big = 14
        else:
            y_big = self.posy + 1
        
        self.clear_spot(x_small, y_small)
        self.clear_spot(x_small, self.posy)
        self.clear_spot(x_small, y_big)
        self.clear_spot(self.posx, y_small)
        self.clear_spot(self.posx, self.posy)
        self.clear_spot(self.posx, y_big)
        self.clear_spot(x_big, y_small)
        self.clear_spot(x_big, self.posy)
        self.clear_spot(x_big, y_big)
    
    def clear_spot(self, posx, posy):
        '''Clear spot posx posy'''
        if self.board[posy][posx] == 0:
            self.board[posy][posx] = 1

    def output(self, string, pair=1):
        '''Outputs messages to the curses screen'''
        self.stdscr.addstr(string + '\n', curses.color_pair(pair))

    def opposite(self, direction):
        '''Returns the opposite direction'''
        opposite = 4 - direction
        if direction % 2 == 0:
            opposite -= 2
        return direction
    
    def move_bear(self):
        '''Move the bear in a random direction'''
        direction = random.randint(0, 3)

        if self.trapped():
            return

        if direction == 0:
            if self.beary > 0:
                self.beary -= 1
        elif direction == 1:
            if self.bearx < 14:
                self.bearx += 1
        elif direction == 2:
            if self.beary < 14:
                self.beary += 1
        elif direction == 3:
            if self.bearx > 0:
                self.bearx -= 1

    def move(self, direction):
        '''Change position on the board'''
        if direction == 0:
            if self.posy > 0:
                self.posy -= 1
                self.moves -= 1
        elif direction == 1:
            if self.posx < 14:
                self.posx += 1
                self.moves -= 1
        elif direction == 2:
            if self.posy < 14:
                self.posy += 1
                self.moves -= 1
        elif direction == 3:
            if self.posx > 0:
                self.posx -= 1
                self.moves -= 1
        
        self.move_bear()
        self.clear_fog()

    def trap(self):
        '''Place a trap at current position'''
        if self.traps > 0:
            self.traps -= 1
            self.board[self.posy][self.posx] = 2
            self.move_bear()
    
    def trapped(self):
        '''See if bear is trapped'''
        return self.board[self.beary][self.bearx] == 2

    def out_of_moves(self):
        return self.moves <= 0
    
    def clear_trees(self):
        if self.can_clear_trees:
            self.can_clear_trees -= 1
            for i in range(15):
                for j in range(15):
                    if abs(self.posy - i) <= 3 and abs(self.posx - j) <= 3:
                        self.clear_spot(j, i)

    def disp(self):
        '''Display the Hunt board'''
        self.stdscr.clear()
        self.output('══════════════════════HUNT═══════════════════════\n')

        if self.trapped():
            self.output('╔═══════════════════════════════════════════════╗')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                 Bear Trapped!                 ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('╚═══════════════════════════════════════════════╝')
        elif self.out_of_moves():
            self.output('╔═══════════════════════════════════════════════╗')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                 Out of Moves!                 ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('║                                               ║')
            self.output('╚═══════════════════════════════════════════════╝')
        else:
            self.output('╔═══════════════════════════════════════════════╗')

            for i in range(15):
                self.stdscr.addstr('║ ')

                for j in range(15):
                    if self.posx == j and self.posy == i:
                        self.stdscr.addstr('   ', curses.color_pair(4))
                    elif i == self.beary and j == self.bearx and self.board[i][j] > 0:
                        if self.trapped():
                            self.stdscr.addstr('###', curses.color_pair(3))
                        else:
                            self.stdscr.addstr('   ', curses.color_pair(3))
                    elif self.board[i][j] == 2:
                        self.stdscr.addstr('###')
                    elif self.board[i][j] == 1:
                        self.stdscr.addstr('   ')
                    else:
                        self.stdscr.addstr('   ', curses.color_pair(2))

                self.stdscr.addstr(' ║\n')

            self.output('╚═══════════════════════════════════════════════╝')
            self.output('')
            self.output('(T)raps Remaining: ' + str(self.traps))
            self.output('Tree (C)lears Remaining: ' + str(self.can_clear_trees))
            self.output('Moves Remaining: ' + str(self.moves))

        self.stdscr.refresh()
            