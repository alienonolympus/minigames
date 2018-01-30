'''Controls the Tic Tac Toe board'''

import curses
import numpy as np

class Board():
    '''The board for Tic Tac Toe'''

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
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1
        self.posy = 1
        self.posx = 1

    def output(self, string, pair=1):
        '''Outputs messages to the curses screen'''
        self.stdscr.addstr(string + '\n', curses.color_pair(pair))

    def opposite(self, direction):
        '''Returns the opposite direction'''
        opposite = 4 - direction
        if direction % 2 == 0:
            opposite -= 2
        return direction
    
    def move(self, direction):
        '''Change position on the board'''
        if direction == 0:
            if self.posy > 0:
                self.posy -= 1
        elif direction == 1:
            if self.posx < 2:
                self.posx += 1
        elif direction == 2:
            if self.posy < 2:
                self.posy += 1
        elif direction == 3:
            if self.posx > 0:
                self.posx -= 1


    def disp(self):
        '''Display the Tic Tac Toe board'''
        self.stdscr.clear()
        self.output('═══════TTT═══════\n')
        self.output('╔═══════════════╗')

        complete = self.complete()

        if complete:
            self.output('║               ║')
            if complete != 3:
                self.output('║ Player ' + str(complete) + ' won! ║')
            else:
                self.output('║      Tie!     ║')
            self.output('║               ║')
        else:
            for i in range(3):
                self.stdscr.addstr('║', curses.color_pair(1))

                for j in range(3):
                    if j == self.posx and i == self.posy: # Current pos
                        if self.player == 1:
                            self.stdscr.addstr('  X  ', curses.color_pair(4))
                        elif self.player == 2:
                            self.stdscr.addstr('  O  ', curses.color_pair(4))
                    elif self.board[i][j]: # Pos with stuff inside
                        if self.board[i][j] == 1:
                            self.stdscr.addstr('  X  ', curses.color_pair(2))
                        elif self.board[i][j] == 2:
                            self.stdscr.addstr('  O  ', curses.color_pair(2))
                    else: # Black pos
                        self.stdscr.addstr('     ', curses.color_pair(1))

                self.stdscr.addstr('║\n', curses.color_pair(1))

        self.output('╚═══════════════╝\n\n')

        self.output('Get three in a row to win')
        self.output('Use arrow keys to move')
        self.output('Use spacebar to place marker')
        self.output('r: Restart')
        self.output('e: Exit')

        self.stdscr.refresh()

    def place(self):
        '''Place the marker down'''
        if not self.board[self.posy][self.posx]:
            self.board[self.posy][self.posx] = self.player
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

    def complete(self):
        '''Check if the game is complete'''
        win_conditions = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        p1_win = False
        p2_win = False
        tie = True

        for condition in win_conditions:
            p1_matching = 0
            p2_matching = 0

            for coord in condition:
                if self.board[coord[0]][coord[1]] == 1:
                    p1_matching += 1
                elif self.board[coord[0]][coord[1]] == 2:
                    p2_matching += 1
                else:
                    tie = False
            
            if p1_matching == 3:
                p1_win = True
            if p2_matching == 3:
                p2_win = True
        
        if p1_win:
            return 1
        elif p2_win:
            return 2
        elif tie:
            return 3
        else:
            return 0
            