# runs as ./Reversi from command line
# chmod +x Reversi makes executable from script
# move = < letter >< number > indicating < column >< row >

import sys
import logging
import argparse
import random
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
    # last_move = '--'    # stores last move

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
        print 'Move played: ' + self.board.last_move
        print self.current_player.color + ' player ( ' + self.current_player.type + ' ) plays now'
        print 'Score: ' + self.computer.color + ' ' + str(self.computer.score) \
              + ' - ' + self.human.color + ' ' + str(self.human.score)

    # switches current player from human to computer or vice versa
    def switch_player(self):
        if self.current_player is self.computer:
            self.current_player = self.human
        else:
            self.current_player = self.computer

    # prompts opponent for a move
    def get_move(self):
        scores = []
        valid = False
        # get human move
        move = raw_input('play < move > : ')
        # get integer coordinate values
        col = self.board.get_col_num(move[0])
        row = self.board.get_row_num(move[1])

        # check row is character in range for board size
        char = row in range(self.size)
        # check column is number in range for board size
        num = col in range(self.size)

        # check move is valid for current game board
        if char and num:
            scores = self.board.check_move(col, row, self.current_player.color[0])
            if len(scores) > 1:
                valid = True
                # self.current_player.current_move = scores
                # self.current_player.score += len(scores) - 1
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
                scores = self.board.check_move(col, row, self.current_player.color[0])
                if len(scores) > 1:
                    valid = True
                    # self.current_player.current_move = scores
                    # self.current_player.score += len(scores) - 1
        return scores

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

            # check if we want to prompt for a move or make one ourselves
            if self.current_player is self.human:
                self.current_player.current_move = self.get_move()
            else:
                self.current_player.current_move = self.board.make_move(self.current_player.color[0])

            # increment score, set move on game board + switch players
            self.current_player.score += len(self.current_player.current_move) - 1
            self.board.set_move(self.current_player.current_move, self.current_player.color[0])
            self.switch_player()


# class to simulate a Reversi game board of given size
class Board:
    size = 8
    board = []
    light = []
    dark = []
    current_neighbs = set()
    last_move = '--'

    # initialize game board of size n
    def __init__(self, n):
        self.size = n
        self.board = self.init_board()

    def set_tile(self, col, row, color):
        self.board[col][row] = color

    def get_tile(self, col, row):
        return self.board[col][row]

    def is_blank(self, col, row):
        if self.get_tile(col, row) is BLANK:
            return True
        else:
            return False

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
        self.update_neighbors(center_1, center_1)
        self.update_neighbors(center_2, center_2)
        self.update_neighbors(center_1, center_2)
        self.update_neighbors(center_2, center_1)

        self.print_tiles()

        return self.board

    # adds new neighbors to set
    def update_neighbors(self, col, row):
        # remove tile if currently in list of available neighbors
        if (col, row) in self.current_neighbs:
                self.current_neighbs.remove((col, row))
        # update neighbor list with new blank boundary tiles
        self.current_neighbs.update(self.get_boundary_list(col, row, True))


    # check move is into valid neighbor space
    def check_move(self, col, row, color):
        scores = []
        if (col, row) not in self.current_neighbs:
            logger.debug('%s not in current_neighbs' % str((col, row)))
            self.print_list(self.current_neighbs)
        else:
            # check for disks in straight lines
            scores = self.check_bounds(col, row, color[0])
            self.last_move = self.display_move(col, row)
        return scores

    # checks bounds for line of bounded opponent disks
    #       +---+---+---+
    #       | 5 | 4 | 3 |
    #       +---+---+---+
    #       | 6 | X | 2 |
    #       +---+---+---+
    #       | 7 | 0 | 1 |
    #       +---+---+---+
    # TODO check if its valid to have move setting disk next to disk of same color to make line
    # TODO that would flip at least one disk, I think it's valid, so need to update code
    # TODO ******* also still not updating all tiles in line although updates score
    # TODO **** look for any neighbors in lines and traverse to those points looking for opp or blank
    # TODO traverse boundary tiles that aren't blank until reaching another blank and check at least 1 opp tile
    def check_bounds(self, col, row, b_color):
        scores = {(col, row)}
        # scores = [(col, row)]
        opp_color = self.get_opp_color(b_color)

        logger.debug('boundary_list for %s' % str((col, row)))
        logger.debug('opp_color  : %s' % opp_color)
        # self.print_list(self.get_boundary_list(col, row))

        # loop through neighbors and check for valid move
        for c, r in self.get_boundary_list(col, row, False):
            move = []
            # if self.get_tile(c, r) is opp_color:
            c_next = c - col
            r_next = r - row
            logger.debug('(c, r)     : %s' % str((c, r)))
            logger.debug('(c_n, r_n) : %s' % str((c + c_next, r + r_next)))
            if self.get_tile(c, r) is opp_color:
                move.append((c, r))
                logger.debug('appending  : %s' % str((c, r)))
            # while self.get_tile(c + c_next, r + r_next) is opp_color or self.get_tile(c + c_next, r + r_next) is b_color:
            # while self.get_tile(c + c_next, r + r_next) is opp_color:
            while self.get_tile(c + c_next, r + r_next) is not BLANK:
                logger.debug('looking at : %s' % str((c + c_next, r + r_next)))
                if self.get_tile(c + c_next, r + r_next) is opp_color:
                    logger.debug('appending  : %s' % str((c + c_next, r + r_next)))
                    move.append((c + c_next, r + r_next))
                c_next += c - col
                r_next += r - row
            # check that move is bounded + flipped at least 1 tile
            if self.get_tile(c + c_next - (c - col), r + r_next - (r - row)) is b_color and len(move) > 0:
                scores.update(move)
            # else:
            #     logger.debug('tile %s is not b_color' % str((c + c_next, r + r_next)))

        return list(scores)

    # TODO may want to loop through light / dark lists to look for tiles in lines
    # check current neighbors for best possible move
    def make_move(self, b_color):
        scores = []
        best_move = []

        # check all available tiles to place a disk + pick best move
        for c, r in self.current_neighbs:
            move = self.check_bounds(c, r, b_color)
            if len(move) > len(best_move):
                best_move = move
            # if len(move) > 1:
            #     scores.append(move)

        # rand = random.randrange(len(scores))
        # print 'scores[rand] : %s' % str(scores[rand][0][0])
        # self.last_move = self.display_move(scores[rand][0][0], scores[rand][0][1])
        self.last_move = self.display_move(best_move[0][0], best_move[0][1])

        return best_move


    def get_minimax(self, b_color):
        my_moves = []
        opp_color = self.get_opp_color(b_color)

        # find all available moves
        for c, r in self.current_neighbs:
            move = self.check_bounds(c, r, b_color)
            if len(move) > 1:
                my_moves.append(move)

        # find all available opposing moves
        # TODO need to simulate updated game board
        for move in my_moves:
            opp_moves = []

            neighbs = self.current_neighbs
            neighbs.update(self.get_boundary_list(move[0][0], move[0][1], True))

            for c, r in neighbs:
                opp_move = self.check_bounds(c, r, opp_color)
                if len(move) > 1:
                    opp_moves.append(opp_move)


     # set move on board + update color, neighbor lists
    def set_move(self, move, color):
        for col, row in move:
            logger.debug('move  : %s' % str((col, row)))
            if color is LIGHT:
                self.light.append((col, row))
            else:
                self.dark.append((col, row))

            # update color lists for flipped disks
            if self.get_tile(col, row) is LIGHT:
                self.light.remove((col, row))
            elif self.get_tile(col, row) is DARK:
                self.dark.remove((col, row))

            # update board + neighbors
            logger.debug('setting %s on board' % str((col, row)))
            self.set_tile(col, row, color)
            self.update_neighbors(col, row)

    def get_opp_color(self, color):
        if color is LIGHT:
            return DARK
        else:
            return LIGHT

    def get_col_num(self, col):
        return ord(col) - 97

    def get_row_num(self, row):
        return int(row) - 1

    def get_boundary_list(self, col, row, blank):
        bounds = []

        if row + 1 in range(self.size) and self.is_blank(col, row - 1) is blank:
            bounds.append((col, row - 1))

        if col + 1 in range(self.size) and self.is_blank(col + 1, row) is blank:
            bounds.append((col + 1, row))

        if col + 1 in range(self.size) and row + 1 in range(self.size) and self.is_blank(col + 1, row + 1) is blank:
            bounds.append((col + 1, row + 1))

        if col + 1 in range(self.size) and row - 1 in range(self.size) and self.is_blank(col + 1, row - 1) is blank:
            bounds.append((col + 1, row - 1))

        if col - 1 in range(self.size) and self.is_blank(col - 1, row) is not BLANK:
            bounds.append((col - 1, row))

        if col - 1 in range(self.size) and row + 1 in range(self.size) and self.is_blank(col - 1, row + 1) is blank:
            bounds.append((col - 1, row + 1))

        if col - 1 in range(self.size) and row - 1 in range(self.size) and self.is_blank(col - 1, row - 1) is blank:
            bounds.append((col - 1, row - 1))

        if row + 1 in range(self.size) and self.is_blank(col, row + 1) is blank:
            bounds.append((col, row + 1))

        return bounds

    # def get_valid_lines(self, col, row):
    #     valid_lines = set()
    #     for c, r in self.current_neighbs:
    #         if c is col or r is row or c - col is r - row:
    #             valid_lines.add((col, row))

    # displays Reversi game board on screen with ASCII art
    def display_board(self):
        print '     a',
        for c in range(self.size - 1):
            print '  ' + chr(ord('b') + c),
        self.print_line()
        for r in range(self.size):
            print ' ' + str(r + 1) + ' |',
            for c in range(self.size):
                print self.get_tile(c, r) + ' |',
            self.print_line()
        print ''

    # prints a horizontal line of dashes + pluses
    def print_line(self):
        line = '\n   +' + '---+' * self.size
        print line[0:self.size * len(line)]

    # returns string representation of move ( ie 'a1', 'd3' )
    def display_move(self, col, row):
        return str(chr(ord('a') + col) + str(row + 1))

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
