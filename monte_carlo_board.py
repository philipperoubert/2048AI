import numpy as np
import random
from termcolor import colored


class Board(object):

    def __init__(self, board=None, points=0):
        if board is None:
            self.board = np.zeros([4, 4]).astype(int)
            self.spawn_number()
            self.spawn_number()
        else:
            self.board = np.copy(board)

        if points == 0:
            self.points = 0
        else:
            self.points = points

    def moves_available(self, get_moves=False):
        """
        Determines whether a move can be made.
        params:
            board: 4x4 np array representing the board.
        returns:
            boolean: True if moves are available or False if not.
        """

        # list containing indexes of 0's
        free_cells = np.where(self.board.reshape(-1) == 0)[0]

        if len(free_cells) > 0 and not get_moves:
            return True

        possible_moves = []

        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j+1] and self.board[i][j] != 0:
                    if "a" not in possible_moves:
                        possible_moves.append("a")
                        possible_moves.append("d")
                    break
                else:
                    if self.board[i][j+1] == 0 and self.board[i][j] != 0:
                        if "d" not in possible_moves:
                            possible_moves.append("d")
                    if self.board[i][j] == 0 and self.board[i][j+1] != 0:
                        if "a" not in possible_moves:
                            possible_moves.append("a")              

        for j in range(4):
            for i in range(3):
                if self.board[i][j] == self.board[i+1][j] and not (self.board[i][j] == 0 and self.board[i+1][j] == 0):
                    if "w" not in possible_moves:
                        possible_moves.append("w")
                        possible_moves.append("s")
                    break
                else:
                    if self.board[i+1][j] == 0 and self.board[i][j] != 0:
                        if "s" not in possible_moves:
                            possible_moves.append("s")
                    if self.board[i][j] == 0 and self.board[i+1][j] != 0:
                        if "w" not in possible_moves:
                            possible_moves.append("w")

        if len(possible_moves) > 0:
            if get_moves:
                return possible_moves
            return True
        return False

    def make_move(self, direction, spawn=True):
        """
        Makes a move on the current board.
        params:
            direction: 'w':up, 'a':left, 's':down, 'd':right
            board: 4x4 np array representing the board.
        returns:
            board: updated 4x4 np array that represents the board, after update
        """
        oldboard = np.copy(self.board)  # makes copy of the initial board state

        if direction == "w":
            # moving up
            self.move_up()

        if direction == "s":
            # down
            self.move_down()

        if direction == "a":
            # left
            self.move_left()

        if direction == "d":
            # right
            self.move_right()

        if (len(np.where(self.board.reshape(-1) == 0)[0]) > 0 and not np.array_equal(self.board, oldboard)):
            if spawn:
                self.spawn_number()

    def move_down(self):
        self.board = self.board.transpose()
        for i in range(4):
            for j in range(1,5):
                if self.board[i][-j] != 0:
                    if 0 in self.board[i][-j:]:
                        self.board[i][-j + (self.board[i][-j:] == 0).sum()] = self.board[i][-j]
                        self.board[i][-j] = 0
            if self.board[i][0] == self.board[i][1] and self.board[i][2] == self.board[i][3]:
                self.board[i][3] *= 2
                self.points += self.board[i][3]
                self.board[i][2] = self.board[i][1] * 2
                self.points += self.board[i][2]
                self.board[i][1] = 0
                self.board[i][0] = 0
            else:
                if self.board[i][1] == self.board[i][2]:
                    self.board[i][2] *= 2
                    self.points += self.board[i][2]
                    self.board[i][1] = 0
                else:
                    for j in range(0,3,2):
                        if self.board[i][j] == self.board[i][j+1]:
                            self.board[i][j+1] *= 2
                            self.points += self.board[i][j+1]
                            self.board[i][j] = 0
            for j in range(1,5):
                if self.board[i][-j] != 0:
                    if 0 in self.board[i][-j:]:
                        self.board[i][-j + (self.board[i][-j:] == 0).sum()] = self.board[i][-j]
                        self.board[i][-j] = 0
        self.board = self.board.transpose()

    def move_up(self):
        self.board = self.board.transpose()
        for i in range(4):
            for j in range(1,4):
                if self.board[i][j] != 0:
                    if 0 in self.board[i][:j]:
                        self.board[i][j - (self.board[i][:j] == 0).sum()] = self.board[i][j]
                        self.board[i][j] = 0
            if self.board[i][0] == self.board[i][1] and self.board[i][2] == self.board[i][3]:
                self.board[i][0] *= 2
                self.points += self.board[i][0]
                self.board[i][1] = self.board[i][2] * 2
                self.points += self.board[i][1]
                self.board[i][2] = 0
                self.board[i][3] = 0
            else:
                if self.board[i][1] == self.board[i][2]:
                    self.board[i][1] *= 2
                    self.points += self.board[i][1]
                    self.board[i][2] = 0
                else:
                    for j in range(0, 3, 2):
                        if self.board[i][j] == self.board[i][j+1]:
                            self.board[i][j] *= 2
                            self.points += self.board[i][j]
                            self.board[i][j+1] = 0
            for j in range(1,4):
                if self.board[i][j] != 0:
                    if 0 in self.board[i][:j]:
                        self.board[i][j - (self.board[i][:j] == 0).sum()] = self.board[i][j]
                        self.board[i][j] = 0
        self.board = self.board.transpose()

    def move_right(self):
        for i in range(4):
            for j in range(1,5):
                if self.board[i][-j] != 0:
                    if 0 in self.board[i][-j:]:
                        self.board[i][-j + (self.board[i][-j:] == 0).sum()] = self.board[i][-j]
                        self.board[i][-j] = 0
            if self.board[i][0] == self.board[i][1] and self.board[i][2] == self.board[i][3]:
                self.board[i][3] *= 2
                self.points += self.board[i][3]
                self.board[i][2] = self.board[i][1] * 2
                self.points += self.board[i][2]
                self.board[i][1] = 0
                self.board[i][0] = 0
            else:
                if self.board[i][1] == self.board[i][2]:
                    self.board[i][2] *= 2
                    self.points += self.board[i][2]
                    self.board[i][1] = 0
                else:
                    for j in range(0,3,2):
                        if self.board[i][j] == self.board[i][j+1]:
                            self.board[i][j+1] *= 2
                            self.points += self.board[i][j+1]
                            self.board[i][j] = 0
            for j in range(1,5):
                if self.board[i][-j] != 0:
                    if 0 in self.board[i][-j:]:
                        self.board[i][-j + (self.board[i][-j:] == 0).sum()] = self.board[i][-j]
                        self.board[i][-j] = 0


    def move_left(self):
        for i in range(4):
            for j in range(1,4):
                if self.board[i][j] != 0:
                    if 0 in self.board[i][:j]:
                        self.board[i][j - (self.board[i][:j] == 0).sum()] = self.board[i][j]
                        self.board[i][j] = 0
            if self.board[i][0] == self.board[i][1] and self.board[i][2] == self.board[i][3]:
                self.board[i][0] *= 2
                self.points += self.board[i][0]
                self.board[i][1] = self.board[i][2] * 2
                self.points += self.board[i][1]
                self.board[i][2] = 0
                self.board[i][3] = 0
            else:
                if self.board[i][1] == self.board[i][2]:
                    self.board[i][1] *= 2
                    self.points += self.board[i][1]
                    self.board[i][2] = 0
                else:
                    for j in range(0, 3, 2):
                        if self.board[i][j] == self.board[i][j+1]:
                            self.board[i][j] *= 2
                            self.points += self.board[i][j]
                            self.board[i][j+1] = 0
            for j in range(1,4):
                if self.board[i][j] != 0:
                    if 0 in self.board[i][:j]:
                        self.board[i][j - (self.board[i][:j] == 0).sum()] = self.board[i][j]
                        self.board[i][j] = 0


    def spawn_number(self, pick_random=True, rand=0, spawn_number=0):
        """
        Picks a random empty cell to spawn a number into it.
        params:
            board: 4x4 np array representing the board.
        returns:
            board: updated 4x4 np array that represents the board, after update
        """
        free_cells = np.where(self.board.reshape(-1) == 0)[0]  # list containing indexes of 0's
        if len(free_cells) > 0:
            # picks a random free spaces to spawn
            if pick_random:
                rand = random.randint(0, len(free_cells) - 1)
            if spawn_number == 0:
                if random.random() < 0.9:
                    # 90% of the time it will spawn a 2
                    self.board.reshape(-1)[free_cells[rand]] = 2
                else:
                    self.board.reshape(-1)[free_cells[rand]] = 4
            else:
                self.board.reshape(-1)[rand] = spawn_number

