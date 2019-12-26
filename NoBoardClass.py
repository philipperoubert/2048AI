import os
import numpy as np
import random
from termcolor import colored


def create_board():
    board = np.zeros([4, 4])
    spawn_number(board)
    spawn_number(board)
    return (board)


def make_move(board, direction, spawn=True):
    oldboard = np.copy(board)
    """
    Makes a move on the current board.
    params:
        direction: 'w':up, 'a':left, 's':down, 'd':right
        board: 4x4 np array representing the board.
    returns:
        board: updated 4x4 np array that represents the board, after update
    """

    if direction == "w":
        # moving up
        new_board = move_up(board)

    if direction == "s":
        # down
        new_board = move_down(board)

    if direction == "a":
        # left
        new_board = move_left(board)

    if direction == "d":
        # right
        new_board = move_right(board)

    if (len(np.where(new_board.reshape(-1) == 0)[0]) > 0 and not np.array_equal(new_board, oldboard)):
        if spawn:
            new_board = spawn_number(new_board)
    return new_board


def rank_board(board):
    x1 = 100  # weighting of highest cell being in top left
    x2 = -2  # weighting on having many free cells
    x3 = 5  # weighting of having many adjacent moves available
    x4 = 100  # weighting of second highest cell being next to highest
    x5 = 1  # weighting of merging the two largest cells
    # x6 = 200 #weighting of merging the third largest cells

    z1 = 0
    i, j = argmax2d(board)
    if in_corner(board, i, j):
        z1 = 1

    free_cells = np.where(board.reshape(-1) == 0)[0]
    z2 = len(free_cells)

    z3 = get_number_adjacent(board)
    z4 = 0
    # z5 = self.points
    locations_second_highest = np.argwhere(board == second_highest(board))
    for h in locations_second_highest:
        if (h[0] == 1 and h[1] == 0):
            z4 = 1

    return (x1 * z1 + x3 * z3 + x4 * z4 + x2 * z2)


def second_highest(board):
    flat = board.flatten()
    flat.sort()
    return flat[-2]


def third_highest(board):
    flat = board.flatten()
    flat.sort()
    return flat[-3]


def get_number_adjacent(board):
    number_adjacent = 0
    number_adjacent += move_up(board, False)
    number_adjacent += move_left(board, False)
    return number_adjacent


def move_up(board, move=True):
    alreadymerged = []
    merge_counter = 0
    # self.points = 0

    for _ in range(3):  # ensures all pieces move as far as they can
        for i in range(1, 4, 1):
            for j in range(4):
                height = i
                while height > 0:  # prevents tiles moving off screen.
                    if board[i - 1][j] == 0 and move:
                        board[i - 1][j] = board[i][j]
                        board[i][j] = 0
                    elif (board[i - 1][j] == board[i][j] and (
                            str(i - 1) + "," + str(j)) not in alreadymerged and (
                                  str(i) + "," + str(j)) not in alreadymerged):
                        if move:
                            board[i - 1][j] *= 2
                            # if (board[i][j] == third_highest(board)):
                            # self.points+=100
                            # self.points += self.board[i - 1][j]
                            board[i][j] = 0

                            # logs tiles which have merged
                            alreadymerged.append(str(i - 1) + "," + str(j))
                            # logs tiles which have merged
                            alreadymerged.append(str(i) + "," + str(j))
                        merge_counter += 1

                    height -= 1
    return board


def move_down(board, move=True):
    merge_counter = 0
    alreadymerged = []
    # self.points = 0
    for _ in range(3):
        for i in range(3, -1, -1):
            for j in range(4):
                height = i
                while height < 3:
                    if board[i + 1][j] == 0 and move:
                        board[i + 1][j] = board[i][j]
                        board[i][j] = 0

                    elif (board[i + 1][j] == board[i][j] and (
                            str(i) + "," + str(j)) not in alreadymerged and (
                                  str(i + 1) + "," + str(j)) not in alreadymerged):
                        if move:
                            board[i + 1][j] *= 2
                            board[i][j] = 0
                            alreadymerged.append(str(i) + "," + str(j))
                            alreadymerged.append(str(i + 1) + "," + str(j))
                        merge_counter += 1
                    height += 1
    return board


def move_left(board, move=True):
    alreadymerged = []
    merge_counter = 0
    for _ in range(3):
        for i in range(4):
            for j in range(4):
                height = j
                while height > 0:
                    if board[i][j - 1] == 0 and move:
                        board[i][j - 1] = board[i][j]
                        board[i][j] = 0

                    elif (board[i][j - 1] == board[i][j] and (
                            str(j) + "," + str(i)) not in alreadymerged and (
                                  str(j - 1) + "," + str(i)) not in alreadymerged):

                        if move:
                            board[i][j - 1] *= 2
                            board[i][j] = 0
                            alreadymerged.append(str(j) + "," + str(i))
                            alreadymerged.append(str(j - 1) + "," + str(i))
                        merge_counter += 1
                    height -= 1
    return board


def move_right(board, move=True):
    alreadymerged = []
    merge_counter = 0

    for _ in range(3):
        for i in range(4):
            for j in range(4, -1, -1):
                height = j
                while height < 3:
                    if board[i][j + 1] == 0:
                        board[i][j + 1] = board[i][j]
                        board[i][j] = 0
                    elif (board[i][j + 1] == board[i][j] and (
                            str(j) + "," + str(i)) not in alreadymerged and (
                                  str(j + 1) + "," + str(i)) not in alreadymerged):
                        if move:
                            board[i][j + 1] *= 2
                            board[i][j] = 0
                            alreadymerged.append(str(j) + "," + str(i))
                            alreadymerged.append(str(j + 1) + "," + str(i))
                        merge_counter += 1
                    height += 1
    return board


def spawn_number(board, pick_random=True, rand=0, spawn_number=0):
    """
    Picks a random empty cell to spawn a number into it.
    params:
        board: 4x4 np array representing the board.
    returns:
        board: updated 4x4 np array that represents the board, after update
    """
    free_cells = np.where(board.reshape(-1) == 0)[0]  # list containing indexes of 0's
    if len(free_cells) > 0:
        # picks a random free spaces to spawn
        if pick_random:
            rand = random.randint(0, len(free_cells) - 1)
        if spawn_number == 0:
            if random.random() < 0.9:
                # 90% of the time it will spawn a 2
                board.reshape(-1)[free_cells[rand]] = 2
            else:
                board.reshape(-1)[free_cells[rand]] = 4
        else:
            board.reshape(-1)[rand] = spawn_number
    return (board)


def free_cells(board):
    """
    Returns the number of free cells, to be used for the AI.
    """
    free_cells = np.where(board.reshape(-1) == 0)[0]  # list containing indexes of 0's
    return free_cells


def in_corner(board, i, j):
    if i == 0 and j == 0:
        return True
    else:
        return False


def argmax2d(board):
    n, m = board.shape
    x_ = np.ravel(board)
    k = np.argmax(x_)
    i, j = k // m, k % m
    return i, j


def moves_available(board, get_moves=False):
    """
    Determines whether a move can be made.
    params:
        board: 4x4 np array representing the board.
    returns:
        boolean: True if moves are available or False if not.
    """

    # list containing indexes of 0's
    free_cells = np.where(board.reshape(-1) == 0)[0]

    if len(free_cells) != 0 and get_moves is False:
        return True

    possible_moves = []
    for move in ["w", "s", "a", "d"]:
        initialboard = np.copy(board)
        make_move(initialboard, move)
        if not np.array_equal(initialboard, board):
            possible_moves.append(move)
        del initialboard

    if get_moves:
        return possible_moves

    if len(possible_moves) > 0:
        return True
    return False


def cls():
    """
    Clears the console (used to make it prettier, not needed in reality)
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def beautify_print(board):
    """
    Prints the board in a prettier way.
    params:
        board: 4x4 np array representing the board.
    """

    color_dict = {0: "red", 2: "green", 4: "yellow", 8: "blue", 16: "magenta", 32: "cyan", 64: "green",
                  128: "yellow", 256: "blue", 512: "magenta", 1024: "cyan", 2048: "green", 5096: "yellow"}
    print("==================")
    for i in range(4):
        print("|", end=" ")
        for j in range(3):
            try:
                print(
                    colored(str(int(board[i][j])), color_dict[int(board[i][j])]), end=" | ")
            except:
                print(board[i][j], end=" | ")
        try:
            print(colored(str(int(board[i][3])),
                          color_dict[int(board[i][3])]), end=" |\n")
        except:
            print(board[i][3], end=" |\n")
        print("==================")


def find_children(board, is_initial=False, is_last=False):
    """
    Find children of a given parent node. Simulates each move (w,a,s,d), and then finds all possible spawn
    possibilities. All these possibilities are considered children of the parent node.
    Parameters:
        board: the parent node being a Board object
        is_initial: Boolean value, to be used in the case we do not want to
                    simulate all possible moves, but just find all possible
                    spawn locations, to be used for depth 1 cases.
    Returns:
        A list of a all children nodes represented by Board objects, List(Board)
    """
    parents = []
    children = []
    if not is_initial:
        for move in moves_available(board, True):
            moved_board = make_move(np.copy(board), move, False)
            parents.append(moved_board)
            del moved_board
    else:
        parents = [board]
    for parent in parents:
        for cell_index in free_cells(parent):
            for two_four in [2]:
                spawned_board = spawn_number(np.copy(parent), pick_random=False, rand=cell_index, spawn_number=two_four)
                if not is_last:
                    children.append(spawned_board)
                else:
                    children.append(rank_board(spawned_board))
                del spawned_board
    return children


if __name__ == "__main__":

    board1 = create_board()  # Initialise a board

    cls()  # using clear function here as it seems that not using it would corrupt the output

    print("Board initialised:")

    while moves_available(board1):
        # cls() # comment this out if you want the program to print out everything
        beautify_print(board1)
        depth = 0
        max_depth = 2
        tree = {"w": [[], []], "a": [[], []], "s": [[], []], "d": [[], []]}  # {move:[[parents][children]]}
        available_moves = moves_available(board1, True)  # Gets a list of all possible moves

        while depth < max_depth:

            # Generate all children nodes
            if depth == 0:  # Initialising the tree dictionary with depth 1 children
                for move in available_moves:
                    moved_board = make_move(np.copy(board1), move)
                    tree[move][1] += find_children(moved_board, True)
                    del moved_board
            if depth == max_depth - 1:
                for move in available_moves:
                    for parent in tree[move][0]:
                        tree[move][1] += find_children(parent, False, True)

            else:
                for move in available_moves:
                    for parent in tree[move][0]:
                        tree[move][1] += find_children(parent)
            depth += 1

            # Determine updated average score for each move
            average_scores = []
            for move in available_moves:
                tree[move][0] = tree[move][1]
                tree[move][1] = []
                average_scores.append(0)
                for i in range(0, len(tree[move][0]), 2):
                    # Probability of 2 * number of points
                    average_scores[-1] += (np.mean(tree[move][0]))
                    # Probability of 4 * number of points
                    # average_scores[-1] += (0.1 * tree[move][0][i+1].points)
                    # 0.5 because we are dividing by the (number of children / 2),
                    # due to multiplying the number of point with the probability
                    # of having a 2 and a 4 per tile.
                if len(tree[move][0]) > 0:
                    average_scores[-1] /= (len(tree[move][0]))
                else:
                    average_scores[-1] = 0
                print("Move " + move + " has an average " + str(average_scores[-1]) + " at depth " + str(depth))

            # Eliminate bad moves
            print("Eliminating bad moves")
            best_move = []
            best_move_avg = 0

            for move in range(len(available_moves)):

                current_move_avg = average_scores[move]
                if best_move_avg == current_move_avg:
                    best_move.append(available_moves[move])
                    best_move_avg = current_move_avg
                elif best_move_avg < current_move_avg:
                    best_move = [available_moves[move]]
                    best_move_avg = current_move_avg
            compare_moves = available_moves[:]
            # for move in compare_moves:
            #    if move not in best_move:
            #        tree[move][0] = []
            #        available_moves.remove(move)
            # Make the move
            print(best_move[0])
            if len(available_moves) == 1:
                board1 = make_move(board1, best_move[0])
                break
            if depth == max_depth:
                print("Running this bit")
                board1 = make_move(board1, best_move[0])

cls()
beautify_print(board1)
# print("Final score: " + str(board1.points))
