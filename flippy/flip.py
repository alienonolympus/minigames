'''Starts a game of flippy'''

from flippy.board import Board

def main(sandbox=False):
    '''Runs flippy'''
    width = 21
    height = 21

    game = Board((height, width), sandbox)

    while True:
        if not sandbox:
            game.generate()
        game.disp()

        while not game.complete() or sandbox:

            key = game.stdscr.getkey()

            if key == 'KEY_UP':
                game.move(0)
            elif key == 'KEY_RIGHT':
                game.move(1)
            elif key == 'KEY_DOWN':
                game.move(2)
            elif key == 'KEY_LEFT':
                game.move(3)
            elif key == 'r':
                if sandbox:
                    game.clear()
                else:
                    game.generate()
            elif key == 'e':
                return

            game.disp()

        while True:
            key = game.stdscr.getkey()

            if key == 'r':
                if sandbox:
                    game.clear()
                    break
                else:
                    game.generate()
                    break
            elif key == 'e':
                return
