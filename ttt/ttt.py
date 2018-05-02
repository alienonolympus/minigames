#/usr/bin/python3
'''Starts a game of Tic Tac Toe'''

from ttt.board import Board

def main():
    '''Runs Tic Tac Toe'''

    game = Board()
    game.disp()

    while True:

        while not game.complete():

            key = game.stdscr.getkey()

            if key == 'KEY_UP':
                game.move(0)
            elif key == 'KEY_RIGHT':
                game.move(1)
            elif key == 'KEY_DOWN':
                game.move(2)
            elif key == 'KEY_LEFT':
                game.move(3)
            elif key == ' ':
                game.place()
            elif key == 'r':
                game = Board()
            elif key == 'e':
                return
            
            game.disp()
        

        key = game.stdscr.getkey()

        if key == 'r':
            game = Board()
        elif key == 'e':
            return

        game.disp()