'''Selection screen for all the minigames'''

import curses
from flippy import flip
from ttt import ttt
from hunt import hunt

def main():
    '''Shows minigames and allow for selection'''

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    minigames = [
        'flippy',
        'flippy sandbox',
        'tictactoe',
        'hunt'
    ]

    descriptions = [
        'Flip all the white tiles in 500 moves',
        'Sandbox version of flippy',
        'Classic 2-Player Tic Tac Toe',
        'Hunt the bear by placing traps'
    ]
    games = len(minigames)
    description = True
    selected = 0

    while True:
        try:
            stdscr.clear()

            stdscr.addstr('MINIGAMES\n\n')

            for i, minigame in enumerate(minigames):
                if selected == i:
                    stdscr.addstr(minigame, curses.color_pair(2))
                    if description:
                        stdscr.addstr(': ' + descriptions[i], curses.color_pair(2))
                    stdscr.addstr('\n', curses.color_pair(2))
                else:
                    stdscr.addstr(minigame + '\n', curses.color_pair(1))

            stdscr.addstr('\nr: Run minigame\n')
            stdscr.addstr('d: Toggle descriptions\n')
            stdscr.addstr('e: Exit menu\n\n\n')

            key = stdscr.getkey()

            if selected > 0:
                if key == 'KEY_UP':
                    selected -= 1

            if selected < games - 1:
                if key == 'KEY_DOWN':
                    selected += 1

            if key == 'r':
                if selected == 0:
                    flip.main()
                elif selected == 1:
                    flip.main(True)
                elif selected == 2:
                    ttt.main()
                elif selected == 3:
                    hunt.main()
            
            if key == 'd':
                description = not description

            if key == 'e':
                break

        except curses.error:
            pass

        except KeyboardInterrupt:
            pass

    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

main()
