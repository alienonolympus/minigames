#/usr/bin/python3
'''Starts a game of flippy'''

from hunt.board import Board

def main(sandbox=False):
    '''Runs flippy'''

    game = Board()

    while True:
        game.disp()
        key = game.stdscr.getkey()
        
        if key == 'KEY_UP':
            game.move(0)
        elif key == 'KEY_RIGHT':
            game.move(1)
        elif key == 'KEY_DOWN':
            game.move(2)
        elif key == 'KEY_LEFT':
            game.move(3)
        elif key == 't':
            game.trap()
        elif key == 'c':
            game.clear_trees()
        elif key == 'r':
            game.__init__()
        elif key == 'e':
            return
