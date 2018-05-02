#/usr/bin/python3
'''Controls platform'''

import random as rd
import curses
import numpy as np
import random

class Board():
    '''The board for platform'''

    def __init__(self, lives_remaining=3):
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
        self.board = np.zeros((10, 60))
        self.next_spike = 5
        self.board[8][20] = 2
        self.posx = 5
        self.posy = 8
        self.y_move_index = 0
        self.y_move_speeds = [0, -3, -2, -1, 0, 1, 2, 3]
        self.score = 0
        self.difficulty = 0
        self.difficulties = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 5), (4, 6), (5, 6), (6, 6)]
        self.game_over = 0
        self.lives_remaining = lives_remaining
        for j in range(60):
            self.board[9][j] = 1

    def output(self, string, pair=1):
        '''Outputs messages to the curses screen'''
        self.stdscr.addstr(string + '\n', curses.color_pair(pair))


    def disp(self):
        '''Displays the board and relevant instructions'''
        self.stdscr.clear()

        if self.lives_remaining == 0:
            self.game_over = 1

        if not(self.game_over):
            for j in range(59):
                self.board[8][j] = self.board[8][j + 1]

            self.next_spike -= 1

            if self.next_spike == 0:
                spikes = random.randint(self.difficulties[self.difficulty][0], self.difficulties[self.difficulty][1])
                for count in range(0, spikes):
                    self.board[8][40 + count] = 2
                self.next_spike = random.randint(10, 17 - spikes)
            
            if 0 < self.y_move_index <= len(self.y_move_speeds) - 1:
                self.posy += self.y_move_speeds[self.y_move_index]
                self.y_move_index += 1
            else:
                self.y_move_index = 0
                self.score += 1
            
            if (self.difficulty + 1) * 50 < self.score and self.difficulty < 10:
                self.difficulty += 1

            for i in range(10):
                for j in range(40):
                    if i == self.posy and j == self.posx and self.board[i][j] == 2:
                        self.stdscr.addstr('  ', curses.color_pair(3))
                        self.lives_remaining -= 1
                    elif i == self.posy and j == self.posx:
                        self.stdscr.addstr('  ', curses.color_pair(4))
                    elif self.board[i][j] == 1:
                        self.stdscr.addstr('██', curses.color_pair(1))
                    elif self.board[i][j] == 2:
                        self.stdscr.addstr('◢◣', curses.color_pair(1))
                    else:
                        self.stdscr.addstr('  ')
                        
                self.stdscr.addstr('\n')
            
            self.output('Score: ' + str(self.score))
            self.output('Score: ' + str(self.lives_remaining))
            self.output('\nJump using the up arrow key\nFall using the down arrow key')
        else:
            self.output('╔═══════════════════════════════════════════╗')
            self.output('║                GAME OVER!                 ║')
            self.output('║                Score: ' + str(self.score) + ' ' * (20 - len(str(self.score))) + '║')
            self.output('║                r: RESTART                 ║')
            self.output('║                e: EXIT                    ║')
            self.output('╚═══════════════════════════════════════════╝')

        self.stdscr.refresh()
