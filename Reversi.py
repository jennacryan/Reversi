# runs as ./Reversi from command line
# chmod +x Reversi makes executable from script
# move = < letter >< number > indicating < column >< row >

import sys
import logging
import argparse
import string

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
log = False


VERSION = 0.1           # version number
AUTHOR = 'Jenna Cryan'  # author
PROGNAME = 'reversi'    # program executable name
VRSNSTR = 'Name     : ' + PROGNAME + '\n Version : ' + str(VERSION) + '\n Author  : ' + AUTHOR     # version info

LIGHT = 'L'             # represents a light disk
DARK = 'D'              # represents a dark disk
BLANK = ' '             # represents a blank disk


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

    # displays information about last move made, whose turn is next + current score
    def display_info(self):
        print 'Move played: ' + self.last_move
        print self.current_player.color + ' player ( ' + self.current_player.type + ' ) plays now'
        print 'Score: ' + self.computer.color + ' ' + str(self.computer.score) \
              + ' - ' + self.human.color + ' ' + str(self.human.score)

    # switches current player from human to computer or vice versa
    def switch_player(self):
        if self.current_player is self.computer:
            self.current_player = self.human
        else:
            self.current_player = self.computer

    def check_move(self, col, row):
        # check move is into valid neighbor space
        if (col, row) not in self.board.current_neighbs:
            logger.debug('%s not in current_neighbs' % str((col, row)))
            self.board.print_list(self.board.current_neighbs)
            return False
        else:
            # check for disks in straight lines
            scores = self.board.check_bounds(col, row, self.current_player.color[0])

            if len(scores) is 1:
                logger.debug('no valid score from move')
                return False
            else:
                self.current_player.current_move = scores
                self.current_player.score += len(scores) - 1
                return True

    # prompts opponent for a move
    def get_move(self):
        valid = False
        # get human move
        move = raw_input('play < move > : ')
        # get integer coordinate values
        col = self.board.get_col_num(move[0])
        row = self.board.get_row_num(move[1])

        # check row is character in range for board size
        char = row < self.size
        # check column is number in range for board size
        num = col < self.size

        # check move is valid for current game board
        if char and num:
            valid = self.check_move(col, row)
        else:
            logger.debug('not char or num')
        while not char or not num or not valid:
            if not char:
                logger.debug('not char')
            elif not num:
                logger.debug('not num')
            elif not valid:
                logger.debug('not valid')

            valid = False
            move = raw_input('Invalid move : ' + move + '\nplay < letter >< number > : ')

            # get integer coordinate values
            col = self.board.get_col_num(move[0])
            row = self.board.get_row_num(move[1])

            # check row, col in size range
            char = col < self.size
            num = row < self.size

            if char and num:
                valid = self.check_move(col, row)
        return move

    # initializes game play with opponent
    def play(self):
        logger.info('Welcome to Reversi!')
        logger.info('')
        self.playing = True
        self.board.init_game()
        # start a new game
        while self.playing:
            self.board.display_board()
            self.display_info()
            self.board.print_list(self.board.current_neighbs)
            # check if we want to prompt for a move or make one ourselves
            if self.current_player is self.human:
                self.last_move = self.get_move()
            # else:
            #     self.last_move = self.board.make_move()
            # # set move on game board + switch players
            self.board.set_move(self.current_player.current_move, self.current_player.color[0])
            self.switch_player()

            self.board.display_board()
            self.display_info()
            self.board.print_list(self.board.current_neighbs)
            self.playing = False


# class to simulate a Reversi game board of given size
class Board:
    size = 8
    board = []
    light = []
    dark = []
    current_neighbs = set()

    # initialize game board of size n
    def __init__(self, n):
        self.size = n
        self.board = self.init_board()

    def set_tile(self, col, row, color):
        self.board[col][row] = color

    def get_tile(self, col, row):
        return self.board[col][row]

    # create a new game board, initially cleared out
    def init_board(self):
        for i in range(self.size):
            self.board.append([' '] * self.size)
        return self.board

    # clears out game board for a new game, with initial center spaces
    def init_game(self):
        # clear board
        for c in range(self.size):
            for r in range(self.size):
                self.set_tile(c, r, BLANK)

        # set up center pieces
        center_1 = self.size / 2 - 1
        center_2 = self.size / 2

        # set color on board + add to color list
        self.set_tile(center_1, center_1, LIGHT)
        self.light.append((center_1, center_1))

        self.set_tile(center_2, center_2, LIGHT)
        self.light.append((center_2, center_2))

        self.set_tile(center_1, center_2, DARK)
        self.dark.append((center_1, center_2))

        self.set_tile(center_2, center_1, DARK)
        self.dark.append((center_2, center_1))

        # add neighbors to available neighbor list
        self.get_neighbors(center_1, center_1)
        self.get_neighbors(center_2, center_2)
        self.get_neighbors(center_1, center_2)
        self.get_neighbors(center_2, center_1)

        self.print_tiles()

        return self.board

    # adds new neighbors to set
    #       +---+---+---+
    #       | 5 | 4 | 3 |
    #       +---+---+---+
    #       | 6 | X | 2 |
    #       +---+---+---+
    #       | 7 | 0 | 1 |
    #       +---+---+---+
    def get_neighbors(self, col, row):
        # remove tile if currently in list of available neighbors
        if (col, row) in self.current_neighbs:
                self.current_neighbs.remove((col, row))

        logger.debug('boundary_list for %s : ' % str((col, row)))
        self.print_list(self.get_boundary_list(col, row))
        for c, r in self.get_boundary_list(col, row):
            if self.get_tile(c, r) is BLANK:
                self.current_neighbs.add((c, r))

    # set move on board + update color, neighbor lists
    def set_move(self, move, color):
        for col, row in move:
            # logger.debug('move : %s' % str(move))
            if color is LIGHT:
                self.light.append((col, row))
            else:
                self.dark.append((col, row))

            # update color lists for flipped disks
            if self.get_tile(col, row) is not BLANK:
                if self.get_tile(col, row) is LIGHT:
                    self.light.remove((col, row))
                else:
                    self.dark.remove((col, row))

            # update board + neighbors
            logger.debug('setting %s on board' % str((col, row)))
            self.set_tile(col, row, color)
            self.get_neighbors(col, row)

    # checks bounds for line of bounded opponent disks
    #       +---+---+---+
    #       | 5 | 4 | 3 |
    #       +---+---+---+
    #       | 6 | X | 2 |
    #       +---+---+---+
    #       | 7 | 0 | 1 |
    #       +---+---+---+
    def check_bounds(self, col, row, b_color):
        score = 0
        scores = [(col, row)]
        opp_color = self.get_opp_color(b_color)

        # loop through neighbors and check for valid move
        logger.debug('boundary_list for %s' % str((col, row)))
        self.print_list(self.get_boundary_list(col, row))
        for c, r in self.get_boundary_list(col, row):
            if self.get_tile(c, r) is opp_color:
                if c >= col and r >= row:
                    score += 1
                else:
                    score -= 1
                scores.append((c, r))
                while self.get_tile(c + score, r) is opp_color:
                    if c >= col and r >= row:
                        score += 1
                    else:
                        score -= 1
                    scores.append((c + score, r))
                if self.get_tile(c + score, r) is not b_color:
                    logger.debug('tile %s is not b_color' % str((c + score, r)))
                    score = 0
                    scores = [(c, r)]
                else:
                    break

        return scores

    # check current neighbors for best possible move
    def make_move(self, b_color):
        scores = []
        opp_color = self.get_opp_color(b_color)

        # check all available tiles to place a disk
        for c, r in self.current_neighbs:
            score = 0
            move = []
            # check all bounds of that tile
            for col, row in self.get_boundary_list(c, r):
                if self.get_tile(col + score, row) is opp_color:
                    score += 1
                    move.append((col, row))
                    while self.get_tile(col + score, row) is opp_color:
                        score += 1
                        move.append((col + score, row))
                    if self.get_tile(col + score, row).color is not b_color:
                        score = 0
                        move = []
                    else:
                        scores.append(move)
        return scores

    def get_opp_color(self, color):
        if color is LIGHT:
            return DARK
        else:
            return LIGHT

    def get_col_num(self, col):
        return ord(col) - 97

    def get_row_num(self, row):
        return int(row) - 1

    def get_boundary_list(self, col, row):
        bounds = []

        bounds.append((col, row + 1))
        bounds.append((col, row - 1))
        bounds.append((col + 1, row))
        bounds.append((col + 1, row + 1))
        bounds.append((col + 1, row - 1))
        bounds.append((col - 1, row))
        bounds.append((col - 1, row + 1))
        bounds.append((col - 1, row - 1))

        return bounds

    # displays Reversi game board on screen with ASCII art
    def display_board(self):
        print '     a',
        for c in range(self.size - 1):
            print '  ' + chr(ord('b') + c),
        self.print_line()
        for r in range(self.size):
            print ' ' + str(c + 1) + ' |',
            for c in range(self.size):
                print self.get_tile(c, r) + ' |',
            self.print_line()
        print ''
        return

    # prints a horizontal line of dashes + pluses
    def print_line(self):
        line = '\n   +' + '---+' * self.size
        print line[0:self.size * len(line)]

    def print_list(self, l):
        logger.debug('list contents ( %d items ) :' % len(l))
        for col, row in l:
            logger.debug(str((col, row)) + '  ' + str(chr(ord('a') + col)) + '' + str(row + 1))

    def print_tiles(self):
        logger.debug('light : ')
        for t in self.light:
            logger.debug(str(t) + '  ' + str(self.get_tile(t[0], t[1])))
        logger.debug('dark : ')
        for t in self.dark:
            logger.debug(str(t) + '  ' + str(self.get_tile(t[0], t[1])))


# class to simulate Reversi player
class Player:
    color = 'Dark'
    type = 'human'
    score = 0
    current_move = []

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
