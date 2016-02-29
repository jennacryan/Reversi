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

LIGHT = 'L'
DARK = 'D'
# move = < letter >< number > indicating < column >< row >

class Reversi:
    playing = False
    light = False
    size = 8
    last_move = '--'


    def __init__(self, n, l):
        self.size = n
        self.board = Board(self.size)
        self.light = l
        if self.light is True:
            self.computer = Player('Dark', 'computer')
            self.human = Player('Light', 'human')
            self.current_player = self.computer
        else:
            self.computer = Player('Light', 'computer')
            self.human = Player('Dark', 'human')
            self.current_player = self.human

    def switch_player(self):
        if self.current_player is self.computer:
            self.current_player = self.human
        else:
            self.current_player = self.computer


# def check_move(self, row, col):
    #     if self.board[row + 1][col] is DARK or self.board[row + 1][col] is DARK

    def get_move(self):
        move = input('play < move > : ')
        char = move[0].isalpha() and move[0] < chr(ord(self.size))
        num = move[1].isdigit() and move[1] < self.size
        while not char or not num:  # or not valid:
            move = input('play < move > : ')
            char = move[0].isalpha() and move[0] < chr(ord(self.size))
            num = move[1].isdigit() and move[1] < self.size
            # valid = self.check_move(move[0], move[1])
        return move[0], move[1]

    def display_info(self):
        print 'Move played: ' + self.last_move
        print self.current_player.color + ' player ( ' \
              + self.current_player.type + ' ) plays now'
        print 'Score: ' + self.computer.color + ' ' + str(self.computer.score) \
              + ' - ' + self.human.color + ' ' + str(self.human.score)

    def play(self):
        logger.info('Welcome to Reversi!')
        logger.info('')
        self.playing = True
        self.board.clear_board()
        # start a new game
        while self.playing:
            self.board.display_board()
            self.display_info()
            # dark goes first
            if self.light is False:
                self.last_move = self.get_move()
                print 'row %d, col %d' % (self.last_move[0], self.last_move[1])
            self.playing = False;
            # else:
            #     row, col = self.make_move()
            # self.set_move(row, col)
            # self.switch_player()



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
        self.board[center_l][center_l] = LIGHT
        self.board[center_h][center_h] = LIGHT
        self.board[center_l][center_h] = DARK
        self.board[center_h][center_l] = DARK

        return self.board

    def display_board(self):
        print '     a',
        for c in range(self.size - 1):
            print '  ' + chr(ord('b') + c),
        self.print_line()
        for x in range(self.size):
            print ' ' + str(x + 1) + ' |',
            for y in range(self.size):
                print self.board[x][y] + ' |',
            self.print_line()
        print ''
        return

    def print_line(self):
        line = '\n   +' + '---+' * self.size
        print line[0:self.size * len(line)]


class Player:
    color = 'Dark'
    type = 'human'
    score = 0

    def __init__(self, color, type):
        self.color = color
        self.type = type


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
