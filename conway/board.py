'''Controls Conway\'s Game of Life'''

import random as rd
import curses
import numpy as np

class Board():
    '''The board for Conway\'s Game of Life'''

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
        self.board = np.zeros((37, 37), dtype=bool)
        self.posx = 18
        self.posy = 18
        self.started = 0
        self.show_neighbours = 0
        self.hold_down = 0

    def output(self, string, pair=1):
        '''Outputs messages to the curses screen'''
        self.stdscr.addstr(string + '\n', curses.color_pair(pair))

    def move(self, direction):
        '''Moves marker'''

        if self.hold_down:
            self.mark()

        if direction == 0:
            if self.posy > 0:
                self.posy -= 1
        elif direction == 1:
            if self.posx < 35:
                self.posx += 1
        elif direction == 2:
            if self.posy < 35:
                self.posy += 1
        elif direction == 3:
            if self.posx > 0:
                self.posx -= 1
    
    def mark(self):
        '''Change the state of current location'''
        self.board[self.posy][self.posx] = not self.board[self.posy][self.posx]

    def neighbours(self, posy, posx):
        '''Return the amount of 'neighbours' of a particular cell'''
        neighbouring = []
        count = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i ** 2 + j ** 2 > 0:
                    neighbouring.append((posy + i, posx + j))
        
        for pos in neighbouring:
            if not(pos[0] < 0 or pos[0] > 35 or pos[1] < 0 or pos[1] > 35):
                count += self.board[pos[0]][pos[1]]
        
        return count

    
    def evolve(self):
        '''Evolve the current board'''
        new_board = np.zeros((37, 37), dtype=bool)

        for i in range(37):
            for j in range(37):
                neighbours = self.neighbours(i, j)
                if self.board[i][j] == 1:
                    if neighbours == 2 or neighbours == 3:
                        new_board[i][j] = 1
                    else:
                        new_board[i][j] = 0
                else:
                    if neighbours == 3:
                        new_board[i][j] = 1
        
        self.board = new_board


    def disp(self):
        '''Displays the board and relevant instructions'''
        self.stdscr.clear()

        self.output('╔' + '═' * 53 + 'CONWAY' + '═' * 52 + '╗')

        for i in range(37):
            self.stdscr.addstr('║')
            for j in range(37):
                if self.show_neighbours:
                    cell_content = ' ' + str(self.neighbours(i, j)) + ' '
                else:
                    cell_content = '   '
                if i == self.posy and j == self.posx and not self.started:
                    if self.board[i][j] == 1:
                        self.stdscr.addstr(cell_content, curses.color_pair(3))
                    else:
                        self.stdscr.addstr(cell_content, curses.color_pair(4))
                elif self.board[i][j] == 1:
                    self.stdscr.addstr(cell_content, curses.color_pair(2))
                else:
                    self.stdscr.addstr(cell_content, curses.color_pair(1))
            self.stdscr.addstr('║\n')

        self.output('╚' + '═' * 111 + '╝\n')

        if not(self.started):
            if not self.hold_down:
                self.output('a: hold pen down          | s: start')
            else:
                self.output('a: lift pen               | s: start')
            self.output('d: show neighbour count   | f: change cell state')
            self.output('r: reset                  | e: exit')
        else:
            self.output('ctrl+c: pause')

        self.stdscr.refresh()
