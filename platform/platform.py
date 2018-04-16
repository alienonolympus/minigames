'''Starts Platformer'''

from platform.board import Board
import curses
from time import sleep

def main():
    '''Runs board'''

    game = Board()
    game.disp()
  
    while True:
        try:
            key = game.stdscr.getkey()
        except curses.error:
            pass
        
        game.disp()
