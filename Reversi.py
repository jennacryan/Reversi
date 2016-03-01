# runs as ./Reversi from command line
# chmod +x Reversi makes executable from script
# move = < letter >< number > indicating < column >< row >

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

LIGHT = 'L'             # represents a light tile
DARK = 'D'              # represents a dark tile
BLANK = ' '             # represents a blank tile


# simulates a game of Reversi
class Reversi:
    playing = False     # signals when game is currently happening
    size = 8            # default board size is 8 x 8
    last_move = '--'    # stores last move

    # initializes game board of size n +
    # human and computer players as light or dark
    def __init__(self, n, l):
        self.size = n
        self.board = Board(self.size)
        if l is True:
            self.human = Player('Light', 'human')
            self.computer = Player('Dark', 'computer')
            self.current_player = self.computer
        else:
            self.computer = Player('Light', 'computer')
            self.human = Player('Dark', 'human')
            self.current_player = self.human

    # switches current player from human to computer or vice versa
    def switch_player(self):
        if self.current_player is self.computer:
            self.current_player = self.human
        else:
            self.current_player = self.computer


# def check_move(self, row, col):
    #     if self.board[row + 1][col] is DARK or self.board[row + 1][col] is DARK

    # prompts opponent for a move
    def get_move(self):
        move = input('play < move > : ')
        char = move[0].isalpha() and move[0] < chr(ord(self.size))
        num = move[1].isdigit() and move[1] < self.size
        while not char or not num:  # or not valid:
            move = input('Invalid move : ' + move + '\nplay < letter >< number > : ')
            char = move[0].isalpha() and move[0] < chr(ord(self.size))
            num = move[1].isdigit() and move[1] < self.size
            # valid = self.check_move(move[0], move[1])
        return move

    # displays information about last move made, whose turn is next, + current score
    def display_info(self):
        print 'Move played: ' + self.last_move
        print self.current_player.color + ' player ( ' + self.current_player.type + ' ) plays now'
        print 'Score: ' + self.computer.color + ' ' + str(self.computer.score) \
              + ' - ' + self.human.color + ' ' + str(self.human.score)

    # initializes game play with opponent
    def play(self):
        logger.info('Welcome to Reversi!')
        logger.info('')
        self.playing = True
        self.board.clear_board()
        # start a new game
        while self.playing:
            self.board.display_board()
            self.display_info()
            # check if we want to prompt for a move or make one ourselves
            if self.current_player is self.human:
                self.last_move = self.get_move()
            self.playing = False
            # else:
            #     row, col = self.make_move()
            # # set move on game board + switch players
            # self.set_move(row, col)
            # self.switch_player()


# class to simulate a Reversi game board of given size
class Board:
    size = 8
    board = []

    # initialize game board of size n
    def __init__(self, n):
        self.size = n
        self.board = self.new_game_board()

    # create a new game board, initially cleared out
    def new_game_board(self):
        for i in range(self.size):
            self.board.append([Tile()] * self.size)
        return self.board

    # clears out game board for a new game, with initial center spaces
    def clear_board(self):
        # clear board
        for x in range(self.size):
            for y in range(self.size):
                self.board[x][y].color = BLANK

        # set up center pieces
        center_1 = self.size / 2 - 1
        center_2 = self.size / 2
        self.board[center_1][center_1].color = LIGHT
        self.board[center_2][center_2].color = LIGHT
        self.board[center_1][center_2].color = DARK
        self.board[center_2][center_1].color = DARK

        return self.board

    # displays Reversi game board on screen with ASCII art
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

    # prints a horizontal line of dashes + pluses
    def print_line(self):
        line = '\n   +' + '---+' * self.size
        print line[0:self.size * len(line)]


# class to simulate a Reversi game board tile as BLANK, LIGHT or DARK
class Tile:
    color = BLANK


# class to simulate Reversi player
class Player:
    color = 'Dark'
    type = 'human'
    score = 0

    # initialize a Player with color + type
    def __init__(self, c, t):
        self.color = c
        self.type = t


# main function to parse command line arguments and create new Reversi game
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

    # create + start a new Reversi game
    game = Reversi(args.size, args.light)
    game.play()


# logs debug message and exits program
def exit_msg(msg):
    logger.debug(msg)
    sys.exit(1)


if __name__ == '__main__':
    main()
