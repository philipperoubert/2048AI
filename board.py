import numpy as np
import random

class Board(object):
    def __init__(self, board=None, points=0):
        if board is None:
            self.board = np.zeros([4, 4])
            self.spawn_number()
            self.spawn_number()
        else:
            self.board = np.copy(board)

        if points == 0:
            self.points = 0
        else:
            self.points = points

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

        if(len(np.where(self.board.reshape(-1) == 0)[0]) > 0 and not np.array_equal(self.board, oldboard)):
            if spawn:
                self.spawn_number()

    def move_up(self):
        alreadymerged = []
        for _ in range(3):  # ensures all pieces move as far as they can
            for i in range(1, 4, 1):
                for j in range(4):
                    height = i
                    while height > 0:  # prevents tiles moving off screen.
                        if self.board[i-1][j] == 0:
                            self.board[i-1][j] = self.board[i][j]
                            self.board[i][j] = 0

                        elif(self.board[i-1][j] == self.board[i][j] and (str(i-1) + "," + str(j)) not in alreadymerged and (str(i) + "," + str(j)) not in alreadymerged):
                            self.board[i-1][j] *= 2
                            self.points += self.board[i-1][j]
                            self.board[i][j] = 0
                            # logs tiles which have merged
                            alreadymerged.append(str(i-1) + "," + str(j))
                            # logs tiles which have merged
                            alreadymerged.append(str(i) + "," + str(j))

                        height -= 1

    def move_down(self):
        alreadymerged = []

        for _ in range(3):
            for i in range(3, -1, -1):
                for j in range(4):
                    height = i
                    while height < 3:
                        if self.board[i+1][j] == 0:
                            self.board[i+1][j] = self.board[i][j]
                            self.board[i][j] = 0

                        elif(self.board[i+1][j] == self.board[i][j] and (str(i) + "," + str(j)) not in alreadymerged and (str(i+1) + "," + str(j)) not in alreadymerged):
                            self.board[i+1][j] *= 2
                            self.points += self.board[i+1][j]
                            self.board[i][j] = 0
                            alreadymerged.append(str(i) + "," + str(j))
                            alreadymerged.append(str(i+1) + "," + str(j))

                        height += 1

    def move_left(self):
        alreadymerged = []

        for _ in range(3):
            for i in range(4):
                for j in range(4):
                    height = j
                    while height > 0:
                        if self.board[i][j-1] == 0:
                            self.board[i][j-1] = self.board[i][j]
                            self.board[i][j] = 0

                        elif(self.board[i][j-1] == self.board[i][j] and (str(j) + "," + str(i)) not in alreadymerged and (str(j-1) + "," + str(i)) not in alreadymerged):
                            self.board[i][j-1] *= 2
                            self.points += self.board[i][j-1]
                            self.board[i][j] = 0
                            alreadymerged.append(str(j) + "," + str(i))
                            alreadymerged.append(str(j-1) + "," + str(i))

                        height -= 1

    def move_right(self):
        alreadymerged = []

        for _ in range(3):
            for i in range(4):
                for j in range(4, -1, -1):
                    height = j
                    while height < 3:
                        if self.board[i][j+1] == 0:
                            self.board[i][j+1] = self.board[i][j]
                            self.board[i][j] = 0

                        elif(self.board[i][j+1] == self.board[i][j] and (str(j) + "," + str(i)) not in alreadymerged and (str(j+1) + "," + str(i)) not in alreadymerged):
                            self.board[i][j+1] *= 2
                            self.points += self.board[i][j+1]
                            self.board[i][j] = 0
                            alreadymerged.append(str(j) + "," + str(i))
                            alreadymerged.append(str(j+1) + "," + str(i))

                        height += 1

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
                rand = random.randint(0, len(free_cells)-1)
            if spawn_number == 0:
                if random.random() < 0.9:
                    # 90% of the time it will spawn a 2
                    self.board.reshape(-1)[free_cells[rand]] = 2
                else:
                    self.board.reshape(-1)[free_cells[rand]] = 4
            else:
                self.board.reshape(-1)[rand] = spawn_number

    def free_cells(self):
        """
        Returns the number of free cells, to be used for the AI.
        """
        free_cells = np.where(self.board.reshape(-1) == 0)[0]  # list containing indexes of 0's
        return free_cells

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

        if len(free_cells) != 0 and get_moves == False:
            return True

        possible_moves = []
        for move in ["w", "s", "a", "d"]:
            initialboard = Board(self.board)
            initialboard.make_move(move)
            if not np.array_equal(initialboard.board, self.board):
                possible_moves.append(move)
            del initialboard

        if get_moves:
            return possible_moves

        if len(possible_moves) > 0:
            return True
        return False
