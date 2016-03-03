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


    # displays information about last move made, whose turn is next, + current score
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


    def check_move(self, row, col):
        # check move is into valid neighbor space
        if (row, col) not in self.board.current_neighbs:
            return False
        else:
            # check for disks in straight lines
            scores = self.board.check_bounds(row, col, self.current_player.color)

            if len(scores) is 0:
                return False
            else:
                self.current_player.current_move = scores
                self.current_player.score += len(scores)
                return True


    # prompts opponent for a move
    def get_move(self):
        valid = False
        move = input('play < move > : ')
        # check row is character and in range for board size
        char = move[0].isalpha() and move[0] < chr(ord(self.size))
        # check column is number and in range for board size
        num = move[1].isdigit() and move[1] < self.size
        # check move is valid for current game board
        if char and num:
            valid = self.check_move(move[0], move[1])
        while not char or not num or not valid:
            valid = False
            move = input('Invalid move : ' + move + '\nplay < letter >< number > : ')
            char = move[0].isalpha() and move[0] < chr(ord(self.size))
            num = move[1].isdigit() and move[1] < self.size
            if char and num:
                valid = self.check_move(move[0], move[1])
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
            # check if we want to prompt for a move or make one ourselves
            if self.current_player is self.human:
                self.last_move = self.get_move()
            # else:
            #     row, col = self.make_move()
            # # set move on game board + switch players
            self.board.set_move(self.current_player.current_move, self.current_player.color)
            self.switch_player()
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

    # create a new game board, initially cleared out
    def init_board(self):
        for i in range(self.size):
            self.board.append([Disk()] * self.size)
        return self.board

    # clears out game board for a new game, with initial center spaces
    def init_game(self):
        # clear board
        for x in range(self.size):
            for y in range(self.size):
                self.board[x][y].color = BLANK

        # set up center pieces
        center_1 = self.size / 2 - 1
        center_2 = self.size / 2

        # set color on board + add to color list
        self.board[center_1][center_1].color = LIGHT
        self.board.light.append((center_1, center_1))

        self.board[center_2][center_2].color = LIGHT
        self.board.light.append((center_2, center_2))

        self.board[center_1][center_2].color = DARK
        self.board.dark.append((center_1, center_2))

        self.board[center_2][center_1].color = DARK
        self.board.dark.append((center_2, center_1))

        # add neighbors to available neighbor list
        self.get_neighbors(center_1, center_1)
        self.get_neighbors(center_2, center_2)
        self.get_neighbors(center_1, center_2)
        self.get_neighbors(center_2, center_1)

        return self.board


    # def set_move(self, row, col):
    #     # ** add play to current color plays list
    #     # ** remove any flipped disks from opposing plays list
    #     # ** remove from neighbors list
    #     # ** update board, flip disks as needed

    def set_move(self, move, color):
        for row, col in move:
            if color is LIGHT:
                self.light.append((row, col))
            else:
                self.dark.append((row, col))

            # update color lists for flipped disks
            if self.board[row][col].color is not BLANK:
                if self.board[row][col].color is LIGHT:
                    self.light.remove((row, col))
                else:
                    self.dark.remove((row, col))

            # update board + neighbors
            self.board[row][col].color = color
            self.get_neighbors(row, col)


    # adds new neighbors to set
    #       +---+---+---+
    #       | 5 | 4 | 3 |
    #       +---+---+---+
    #       | 6 | X | 2 |
    #       +---+---+---+
    #       | 7 | 0 | 1 |
    #       +---+---+---+
    def get_neighbors(self, row, col):
        # remove tile if currently in list of available neighbors
        if (row, col) in self.board.current_neighbs:
                self.board.current_neighbs.remove((row, col))

        # ( 0 ) check S neighbor
        if self.board[row + 1][col].blank is True:
            self.current_neighbs.add((row + 1, col))
        # ( 1 ) check SE neighbor
        if self.board[row + 1][col + 1].blank is True:
            self.current_neighbs.add((row + 1, col + 1))
        # ( 2 ) check E neighbor
        if self.board[row][col + 1].blank is True:
            self.current_neighbs.add((row, col + 1))
        # ( 3 ) check NE neighbor
        if self.board[row - 1][col + 1].blank is True:
            self.current_neighbs.add((row - 1, col + 1))
        # ( 4 ) check N neighbor
        if self.board[row - 1][col].blank is True:
            self.current_neighbs.add((row - 1, col))
        # ( 5 ) check NW neighbor
        if self.board[row - 1][col - 1].blank is True:
            self.current_neighbs.add((row - 1, col - 1))
        # ( 6 ) check W neighbor
        if self.board[row][col - 1].blank is True:
            self.current_neighbs.add((row, col - 1))
        # ( 7 ) check SW neighbor
        if self.board[row + 1][col - 1].blank is True:
            self.current_neighbs.add((row + 1, col - 1))


    # adds bounding tiles to list
    #       +---+---+---+
    #       | 5 | 4 | 3 |
    #       +---+---+---+
    #       | 6 | X | 2 |
    #       +---+---+---+
    #       | 7 | 0 | 1 |
    #       +---+---+---+
    def check_bounds(self, row, col, b_color):
        score = 0
        scores = []
        opp_color = self.get_opp_color(b_color)

        # ( 0 ) check S neighbor
        if self.board[row + 1][col].color is opp_color:
            score += 1
            scores.append((row + 1, col))
            while self.board[row + 1 + score][col].color is opp_color:
                score += 1
                scores.append((row + 1 + score, col))
            if self.board[row + 1 + score][col].color is not b_color:
                score = 0
                scores = []
            else:
                return scores

        # ( 1 ) check SE neighbor
        if self.board[row + 1][col + 1].color is opp_color:
            score += 1
            scores.append((row + 1, col + 1))
            while self.board[row + 1 + score][col + 1 + score].color is opp_color:
                score += 1
                scores.append((row + 1 + score, col + 1 + score))
            if self.board[row + 1][col + 1 + score].color is not b_color:
                score = 0
                scores = []
            else:
                return scores

        # ( 2 ) check E neighbor
        if self.board[row][col + 1].color is opp_color:
            score += 1
            scores.append((row, col + 1))
            while self.board[row][col + 1 + score].color is opp_color:
                score += 1
                scores.append((row, col + 1 + score))
            if self.board[row][col + 1 + score].color is not b_color:
                score = 0
                scores = []
            else:
                return scores

        # ( 3 ) check NE neighbor
        if self.board[row - 1][col + 1].color is opp_color:
            score += 1
            scores.append((row - 1, col + 1))
            while self.board[row - 1 - score][col + 1 + score].color is opp_color:
                score += 1
                scores.append((row - 1 - score, col + 1 + score))
            if self.board[row - 1 - score][col + 1 + score].color is not b_color:
                score = 0
                scores = []
            else:
                return scores

        # ( 4 ) check N neighbor
        if self.board[row - 1][col].color is opp_color:
            score += 1
            scores.append((row - 1, col))
            while self.board[row + 1 + score][col].color is opp_color:
                score += 1
                scores.append((row - 1 - score, col))
            # if self.board[row + 1 + score][col].color is not b_color:
            #     score = 0
            return scores

        # ( 5 ) check NW neighbor
        if self.board[row - 1][col - 1].color is opp_color:
            score += 1
            scores.append((row - 1, col - 1))
            while self.board[row - 1 - score][col - 1 - score].color is opp_color:
                score += 1
                scores.append((row - 1 - score, col - 1 - score))
            if self.board[row - 1 - score][col - 1 - score].color is not b_color:
                score = 0
                scores = []
            else:
                return scores

        # ( 6 ) check W neighbor
        if self.board[row][col - 1].color is opp_color:
            score += 1
            while self.board[row][col - 1 - score].color is opp_color:
                score += 1
            if self.board[row][col - 1 - score].color is not b_color:
                score = 0
                scores = []
            else:
                return scores

        # ( 7 ) check SW neighbor
        if self.board[row + 1][col - 1].color is opp_color:
            score += 1
            scores.append((row + 1, col - 1))
            while self.board[row + 1 + score][col - 1 - score].color is opp_color:
                score += 1
                scores.append((row + 1 + score, col - 1 - score))
            if self.board[row + 1 + score][col - 1 - score].color is not b_color:
                score = 0
                scores = []

        return scores


    def get_opp_color(self, color):
        if color is LIGHT:
            return DARK
        else:
            return LIGHT


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


# class to simulate a BLANK, LIGHT or DARK disk on a Reversi game board
class Disk:
    color = BLANK

    # checks if tile has no disk currently occupying it
    def blank(self):
        if self.color is BLANK:
            return True
        else:
            return False

    # checks if tile currently contains a light disk
    def light(self):
        if self.color is LIGHT:
            return True
        else:
            return False

    # checks if tile currently contains a dark disk
    def dark(self):
        if self.color is DARK:
            return True
        else:
            return False


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
