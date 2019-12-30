import os
import numpy as np
import random
from termcolor import colored


def create_board():
    board = np.zeros([4, 4])
    spawn_number(board)
    spawn_number(board)
    return board


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
    x1 = 40 # weighting of highest cell in corner edge
    x2 = 20 # weighting on having many free cells
    #x3 = 1 # weighting of having many adjacent moves available
    x4 = 5 # weighting of second largest on edge
    #x5 = 1 # not monotonic



    z1=0
    i, j = argmax2d(board)
    if(i==0 and j == 0):
        z1 = 1
    
    free_cells = np.where(board.reshape(-1) == 0)[0]
    z2 = len(free_cells)

    z3 = get_number_adjacent(board)

    # z5 = self.points
    z4=0
    locations_second_highest = np.argwhere(board == nhighest(board,2))
    for h in locations_second_highest:
        if (h[0] == 0 or h[0] == 3 or h[1] == 0 or h[1] ==3):
            z4 = 1

    #z5 = get_gradient(board)



    return (x1*z1 + x2*z2 + x4*z4 + np.max(board))

def new_highest(board, oldboard):
    if(np.amax(board) > np.amax(oldboard)):
        return 1
    return 0

def get_gradient(board):
    deficit = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j+1]>board[i][j]):
                deficit-=board[i][j+1]

    for i in range(3):
        for j in range(3):
            if(board[i+1][j] > board[i][j]):
                deficit -=board[i+1][j]
    return(deficit)
def nhighest(board,x):
    flat = board.flatten()
    flat.sort()
    return flat[-x]



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
    if move:
        return board
    else:
        return(merge_counter)


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
    if move:
        return board
    else:
        return (merge_counter)


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
    if move:
        return board
    else:
        return (merge_counter)


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
    if move:
        return board
    else:
        return (merge_counter)


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


if __name__ == "__main__":

    board1 = create_board()  # Initialise a board

    cls()  # using clear function here as it seems that not using it would corrupt the output

    print("Board initialised:")

    while moves_available(board1):
        # cls() # comment this out if you want the program to print out everything
        beautify_print(board1)
        depth = 0
        max_depth = 500
        final_scores = np.zeros(4)

        for _ in range(50):
            newer_board = np.copy(board1)
            l=0
            while moves_available(newer_board) and l < max_depth:

                available_moves = moves_available(newer_board, True)  # Gets a list of all possible moves
                move_to_make = random.choice(available_moves)


                newer_board = make_move(newer_board, move_to_make)
                if(l == 0):
                    first_move = move_to_make
                l+=1



        if(first_move=="w"):
            final_scores[0] += rank_board(newer_board)
        if (first_move == "a"):
            final_scores[1] += rank_board(newer_board)
        if (first_move == "s"):
            final_scores[2] += rank_board(newer_board)
        if (first_move == "d"):
            final_scores[3] += rank_board(newer_board)

        best_move = np.argmax(final_scores)

        if(best_move == 0):
            best_move = "w"
        if(best_move==1):
            best_move = "a"
        if(best_move==2):
            best_move = "s"
        if(best_move==3):
            best_move="d"

        print(best_move)
        board1 = make_move(board1, best_move, True)


cls()
beautify_print(board1)
# print("Final score: " + str(board1.points))
