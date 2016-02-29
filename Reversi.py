# runs as ./Reversi from command line
# chmod +x Reversi makes executable from script

import sys
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
log = True


VERSION = 0.1           # version number
AUTHOR = 'Jenna Cryan'  # author
PROGNAME = 'reversi'    # program executable name
VRSNSTR = 'Name     : ' + PROGNAME + '\n Version : ' + str(VERSION) + '\n Author  : ' + AUTHOR     # version info


class Reversi:
    playing = False
    light = False

    def __init__(self, n, l):
        self.board = Board(n)
        self.light = l

    def play(self):
        logger.info('Welcome to Reversi!')
        self.playing = True
        if self.light is True:
            logger.info('It"s your turn first!')
        # while self.playing:
        self.board.clear_board()
        self.board.display_board()


class Board:
    size = 8
    board = []

    def __init__(self, n):
        self.size = n
        self.board = self.new_game_board()

    def new_game_board(self):
        for i in range(self.size):
            self.board.append([' '] * self.size)
        return self.board

    def clear_board(self):
        # clear board
        for x in range(self.size):
            for y in range(self.size):
                self.board[x][y] = ' '

        # set up center pieces
        center_l = self.size / 2 - 1
        center_h = self.size / 2
        self.board[center_l][center_l] = 1
        self.board[center_h][center_h] = 1
        self.board[center_l][center_h] = 0
        self.board[center_h][center_l] = 0

        return self.board

    def display_board(self):
        print '   |  a',
        for c in range(self.size - 1):
            print ' |  ' + chr(ord('b') + c),
        print ' |',
        self.print_line()
        for x in range(self.size):
            print ''
            print ' ' + str(x + 1) + ' |',
            for y in range(self.size):
                print '  ' + str(self.board[x][y]) + ' |',
            self.print_line()
        return

    def print_line(self):
        print '\n   ',
        for i in range(self.size):
            print '-----',


def main():

    parseargs = argparse.ArgumentParser()

    parseargs.add_argument('-v', '--version', action='version', version=VRSNSTR,
                           help='print version and author information and exit')
    parseargs.add_argument('-n', '--size', default=8, type=int,
                           help='specify board size ( even number in range 4-26, default = 8 x 8 )')
    parseargs.add_argument('-l', '--light', action='store_true',
                           help='specify to play with light colors, default is dark colors')
    args = parseargs.parse_args()

    if args.size < 4 or args.size > 27 or args.size % 2 is not 0:
        exit_msg('Invalid board size : %d' % args.size)

    game = Reversi(args.size, args.light)
    game.play()


def exit_msg(msg):
    logger.debug(msg)
    sys.exit(1)


if __name__ == '__main__':
    main()
