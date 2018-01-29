'''Controls how the board of flippy works'''

import random as rd
import curses
import numpy as np

class Board():
    '''The board for flippy'''

    def __init__(self, size, sandbox):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.size = size
        self.position = [rd.randint(0, size[0] - 1), rd.randint(0, size[1] - 1)]
        self.board = np.zeros(size, dtype=bool)
        self.sandbox = sandbox
        self.moves = 0
        self.target = 0

    def output(self, string, pair=1):
        '''Outputs messages to the curses screen'''
        self.stdscr.addstr(string + '\n', curses.color_pair(pair))

    def pos(self):
        '''Returns the value of the marker's current position'''
        return self.board[self.position[0]][self.position[1]]

    def opposite(self, direction):
        '''Returns the opposite direction'''
        opposite = 4 - direction
        if direction % 2 == 0:
            opposite -= 2
        return direction

    def move(self, direction):
        '''Moves marker'''

        # Exits if crosses boundary
        if (self.position[0] == 0) and (direction == 0):
            return
        if (self.position[1] == self.size[1] - 1) and (direction == 1):
            return
        if (self.position[0] == self.size[0] - 1) and (direction == 2):
            return
        if (self.position[1] == 0) and (direction == 3):
            return

        # Inverts current position
        if self.pos() < 2:
            self.board[self.position[0]][self.position[1]] = not self.pos()

        # Alters current position
        if direction == 0:
            self.position[0] -= 1
        elif direction == 1:
            self.position[1] += 1
        elif direction == 2:
            self.position[0] += 1
        elif direction == 3:
            self.position[1] -= 1

        self.moves += 1

    def unflipped(self):
        '''Returns number of unflipped blocks'''
        blocks = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i, j] == 1:
                    blocks += 1
        return blocks

    def disp(self):
        '''Displays the board and relevant instructions'''
        self.stdscr.clear()
        self.output('═══════════════════FLIP.PY═══════════════════')
        self.output('\n')

        if self.complete() and not self.sandbox:
            if self.moves < self.target:
                self.output('╔═══════════════════════════════════════════╗')
                self.output('║               GAME COMPLETE!              ║')
                self.output('╚═══════════════════════════════════════════╝')
                self.output('')
                self.output('Moves remaining: ' + str(self.target - self.moves))
            else:
                self.output('╔═══════════════════════════════════════════╗')
                self.output('║                GAME FAILED!               ║')
                self.output('╚═══════════════════════════════════════════╝')
                self.output('')
                self.output('Blocks remaining: ' + str(self.unflipped()))
        else:
            self.output('╔' + '═' * (self.size[1] * 2 + 1) + '╗')

            for i in range(self.size[0]):
                self.stdscr.addstr('║ ', curses.color_pair(1))
                for j in range(self.size[1]):
                    if self.position == [i, j]: # Marker
                        self.stdscr.addstr('  ', curses.color_pair(4))
                    elif self.board[i, j] == 2: # Starting pos (ignored pos)
                        self.stdscr.addstr('  ', curses.color_pair(3))
                    elif self.board[i][j]: # Flipped
                        self.stdscr.addstr('  ', curses.color_pair(2))
                    else: # Unflipped
                        self.stdscr.addstr('  ', curses.color_pair(1))
                self.stdscr.addstr('║\n', curses.color_pair(1))

            self.output('╚' + '═' * (self.size[1] * 2 + 1) + '╝')
            self.output('')
            if not self.sandbox:
                self.output('Moves left: ' + str(self.target - self.moves))
            self.output('')
            self.output('Instructions:')
            self.output('Press the arrow keys to move the green marker')
            self.output('The marker flips the spot its leaves')
            self.output('Flip the whole board so it is black')

        self.output('')
        if self.sandbox:
            self.output('r: Clear')
        else:
            self.output('r: Restart')
        self.output('e: exit')

        self.stdscr.refresh()

    def generate(self):
        '''Random generates a game'''
        self.position = [rd.randint(0, self.size[0] - 1), rd.randint(0, self.size[1] - 1)]
        self.board = np.zeros(self.size, dtype=int)
        self.moves = 0

        '''count = 0
        while True:
            self.move(rd.randint(0, 3), True)
            count += 1

            if count > 3000 and self.pos():
                break'''

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.board[i][j] = rd.randint(0, 1)

        self.board[self.position[0]][self.position[1]] = 2 # Sets starting pos (ignored pos)
        self.target = 500 # Sets target number of moves

    def complete(self):
        '''Check if grid is complete or if too many moves are attempted'''
        if self.moves > self.target:
            return True

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i, j] == 1:
                    return False

        return True

    def clear(self):
        '''Clears board in sandbox mode'''
        self.board = np.zeros(self.size, dtype=bool)
