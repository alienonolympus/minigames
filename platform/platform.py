#/usr/bin/python3
'''Starts Platformer'''

from platform.board import Board
import curses
from time import sleep

def main(lives_remaining=3):
    '''Runs board'''

    game = Board(lives_remaining)
    game.disp()
  
    while True:
        try:
            key = game.stdscr.getkey()
            if not(game.game_over):
                if key == 'KEY_UP' and game.posy == 8:
                    game.y_move_index = 1
                elif key == 'KEY_DOWN':
                    game.y_move_index = 0
                    game.posy = 8
            else:
                if key == 'e':
                    break
                elif key == 'r':
                    game = Board()
        except curses.error:
            pass
        
        game.disp()
