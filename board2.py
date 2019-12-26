import numpy as np
import random


class Board(object):

    def __init__(self, board=None, points=0):
        if board is None:
            # 0 (n) is a 4-bit int that represents the 2 ^ n value
            # * 4 (rows) * 4 (collumns)
            self.board = [0] * 4 * 4
            self.spawn_number()
            self.spawn_number()
        else:
            self.board = board[:]

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
        oldboard = self.board[:] # makes copy of the initial board state

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

        if 0 in self.board and self.board != oldboard:
            if spawn:
                self.spawn_number()

        self.points = self.rank_board()


    def rank_board(self):

        x1 = 130 #weighting of highest cell being in top left
        x2 = -2 #weighting on having many free cells
        x3 = 5 #weighting of having many adjacent moves available
        x4 = 60 #weighting of second highest cell being next to highest
        x5 = 1  #weighting of merging the two largest cells
        #x6 = 200 #weighting of merging the third largest cells

        z1=0
        if self.board.index(max(self.board)) == 0:
            z1 = 1

        z2 = self.board.count(0)


        z3 = self.get_number_adjacent()



        return x1*z1 + x2*z2 + x3 + z3

        locations_second_highest = [i for i, x in enumerate(self.board) if x == self.second_highest()]
        for h in locations_second_highest:
            if h == 4:
                z4 = 1

        return (x1*z1 + x3*z3 + x4*z4 + x2*z2)

    #     #
    #     # z4 = 0
    #     # z5 = self.points
    #     # locations_second_highest = np.argwhere(self.board == self.second_highest())
    #     # for h in locations_second_highest:
    #     #     if (h[0] == 1 and h[1] == 0):
    #     #         z4 = 1

    #     # return (x1*z1 + x3*z3 + x4*z4 + x5*z5 + x2*z2)

    def second_highest(self):
        return sorted(self.board)[-2]

    # def third_highest(self):
    #     flat = self.board.flatten()
    #     flat.sort()
    #     return (flat[-3])

    def get_number_adjacent(self):
        total_mergers = 0
        for i in range(4):
            row_merger = 0
            if self.board[i * 4] == self.board[i * 4 + 1]:
                row_merger += 1
            if self.board[i * 4 + 2] == self.board[i * 4 + 3]:
                row_merger += 1
            if row_merger == 0:
                if self.board[i * 4 + 1] == self.board[i * 4 + 2]:
                    row_merger += 1
            total_mergers += row_merger
        for j in range(4):
            column_merger = 0
            if self.board[j] == self.board[j + 4 * 1]:
                column_merger += 1
            if self.board[j + 4 * 2] == self.board[j + 4 * 3]:
                column_merger += 1
            if column_merger == 0:
                if self.board[j + 4 * 1] == self.board[j + 4 * 2]:
                    column_merger += 1
            total_mergers += column_merger
        return total_mergers


    def move_up(self, move=True):
        alreadymerged = []
        merge_counter = 0
        self.points = 0

        for _ in range(3):  # ensures all pieces move as far as they can
            for i in range(1, 4, 1):
                for j in range(4):
                    height = i
                    while height > 0:  # prevents tiles moving off screen.
                        if self.board[(i - 1) * 4 + j] == 0 and move:
                            self.board[(i - 1) * 4 + j] = self.board[i * 4 + j]
                            self.board[i * 4 + j] = 0
                        elif self.board[(i - 1) * 4 + j] == self.board[i * 4 + j] and (i-1) * 4 + j not in alreadymerged and i * 4 + j not in alreadymerged:
                            if move:

                                self.board[(i - 1) * 4 + j] += 1
                                #if (self.board[i * 4 + j] == self.third_highest()):
                                #    self.points+=100
                                #self.points += self.board[i - 1][j]
                                self.board[i * 4 + j] = 0

                                # logs tiles which have merged
                                alreadymerged.append((i-1) * 4 + j)
                                # logs tiles which have merged
                                alreadymerged.append(i * 4 + j)
                            merge_counter += 1

                        height -= 1
        return merge_counter

    def move_down(self, move=True):
        merge_counter = 0
        alreadymerged = []
        self.points = 0
        for _ in range(3):
            for i in range(3, -1, -1):
                for j in range(4):
                    height = i
                    while height < 3:
                        if self.board[(i + 1) * 4 + j] == 0 and move:
                            self.board[(i + 1) * 4 + j] = self.board[i * 4 + j]
                            self.board[i * 4 + j] = 0

                        elif self.board[(i + 1) * 4 + j] == self.board[i * 4 + j] and i * 4 + j not in alreadymerged and (i+1) * 4 + j not in alreadymerged:
                            if move:
                                self.board[(i + 1) * 4 + j] += 1
                                #if (self.board[i][j] == self.third_highest()):
                                #    self.points += 100
                                #self.points += self.board[i + 1][j]
                                self.board[i * 4 + j] = 0
                                alreadymerged.append(i * 4 + j)
                                alreadymerged.append(i+1 * 4 + j)
                            merge_counter += 1
                        height += 1
        return merge_counter

    def move_left(self, move=True):
        alreadymerged = []
        merge_counter = 0
        self.points = 0
        for _ in range(3):
            for i in range(4):
                for j in range(4):
                    height = j
                    while height > 0:
                        if self.board[i * 4 + j - 1] == 0 and move:
                            self.board[i * 4 + j - 1] = self.board[i * 4 + j]
                            self.board[i * 4 + j] = 0

                        elif self.board[i * 4 + j - 1] == self.board[i * 4 + j] and i * 4 + j not in alreadymerged and i * 4 + j - 1 not in alreadymerged:

                            if move:
                                self.board[i * 4 + j - 1] += 1
                                #if (self.board[i * 4 + j] == self.third_highest()):
                                #    self.points += 100
                                #self.points += self.board[i][j - 1]

                                self.board[i * 4 + j] = 0
                                alreadymerged.append(i * 4 + j)
                                alreadymerged.append(i * 4 + j - 1)
                            merge_counter += 1
                        height -= 1
        return merge_counter

    def move_right(self, move=True):
        alreadymerged = []
        merge_counter = 0
        self.points = 0
        for _ in range(3):
            for i in range(4):
                for j in range(4, -1, -1):
                    height = j
                    while height < 3:
                        if self.board[i * 4 + j + 1] == 0:
                            self.board[i * 4 + j + 1] = self.board[i * 4 + j]
                            self.board[i * 4 + j] = 0
                        elif self.board[i * 4 + j + 1] == self.board[i * 4 + j] and i * 4 + j not in alreadymerged and i * 4 + j + 1 not in alreadymerged:
                            if move:
                                self.board[i * 4 + j + 1] += 1
                                #self.points += self.board[i * 4 + j + 1]
                                #if (self.board[i][j] == self.third_highest()):
                                #    self.points += 100
                                self.board[i * 4 + j] = 0
                                alreadymerged.append(i * 4 + j)
                                alreadymerged.append(i * 4 + j + 1)
                            merge_counter += 1
                        height += 1
        return merge_counter

    def spawn_number(self, pick_random=True, rand=0, spawn_number=0):
        """
        Picks a random empty cell to spawn a number into it.
        params:
            board: 4x4 np array representing the board.
        returns:
            board: updated 4x4 np array that represents the board, after update
        """
        free_cells = [i for i, x in enumerate(self.board) if x == 0]
        if len(free_cells) > 0:
            # picks a random free spaces to spawn
            if pick_random:
                rand = random.randint(0, len(free_cells) - 1)
            if spawn_number == 0:
                if random.random() < 0.9:
                    # 90% of the time it will spawn a 2
                    self.board[free_cells[rand]] = 1
                else:
                    self.board[free_cells[rand]] = 2
            else:
                self.board[rand] = spawn_number

    def free_cells(self):
        """
        Returns the number of free cells, to be used for the AI.
        """
        free_cells = [i for i, x in enumerate(self.board) if x == 0]  # list containing indexes of 0's
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

        if 0 in self.board and get_moves is False:
            return True

        possible_moves = []
        for move in ["w", "s", "a", "d"]:
            initial_board = Board(self.board)
            initial_board.make_move(move)
            if initial_board.board != self.board:
                possible_moves.append(move)
            del initial_board

        if get_moves:
            return possible_moves

        if len(possible_moves) > 0:
            return True
        return False
