'''Starts Conway\'s Game of Life'''

from conway.board import Board
from time import sleep

def main():
    '''Runs Conway\'s Game of Life'''

    game = Board()
  
    while True:
        if not game.started:
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
            elif key == 'f':
                game.mark()
            elif key == 's':
                game.started = 1
            elif key == 'd':
                game.show_neighbours = not game.show_neighbours
            elif key == 'a':
                game.hold_down = not game.hold_down
            elif key == 'r':
                game.__init__()
            elif key == 'e':
                return
        else:
            try:
                # See if everyone died
                total = 0
                for i in range(36):
                    for j in range(36):
                        total += game.board[i][j]
                if total == 0:
                    game.started = 0

                sleep(0.5)
                game.disp()
                game.evolve()

            except KeyboardInterrupt:
                game.started = 0
