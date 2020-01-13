import os
from board_with_heuristics import Board
from termcolor import colored


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

    color_dict = {0: "red", 2: "green", 4: "yellow", 8: "blue", 16: "magenta", 32: "cyan",
                  64: "green", 128: "yellow", 256: "blue", 512: "magenta", 1024: "cyan",
                  2048: "green", 5096: "yellow"}
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


def find_children(board, is_initial=False):
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
        for move in board.moves_available(True):
            moved_board = Board(board.board, board.points)
            moved_board.make_move(move, False)
            parents.append(moved_board)
            del moved_board
    else:
        parents = [board]
    for parent in parents:
        for cell_index in parent.free_cells():
            for two_four in [2]:
                spawned_board = Board(parent.board, parent.points)
                spawned_board.spawn_number(pick_random=False, rand=cell_index, spawn_number=two_four)
                children.append(spawned_board)
                del spawned_board
    return children


if __name__ == "__main__":

    for i in range(5000):

        board1 = Board()  # Initialise a board

        cls()  # using clear function here as it seems that not using it would corrupt the output

        print("Board initialised:")

        while board1.moves_available():
            # cls() # comment this out if you want the program to print out everything
            #beautify_print(board1.board)
            depth = 0
            max_depth = 2
            # {move:[[parents][children]]}
            tree = {"w": [[], []], "a": [[], []], "s": [[], []], "d": [[], []]}  
            available_moves = board1.moves_available(True)  # Gets a list of all possible moves

            while depth < max_depth:

                # Generate all children nodes
                if depth == 0:  # Initialising the tree dictionary with depth 1 children
                    for move in available_moves:
                        moved_board = Board(board1.board, board1.points)
                        moved_board.make_move(move, False)
                        tree[move][1] += find_children(board=moved_board, is_initial=True)
                        del moved_board
                else:
                    for move in available_moves:
                        for parent in tree[move][0]:
                            tree[move][1] += find_children(board=parent)
                depth += 1

                # Determine updated average score for each move
                average_scores = []
                for move in available_moves:
                    tree[move][0] = tree[move][1]
                    tree[move][1] = []
                    average_scores.append(0)
                    for i in range(0, len(tree[move][0]), 2):
                        # Probability of 2 * number of points
                        average_scores[-1] += (1.0 * tree[move][0][i].points)
                        # Probability of 4 * number of points
                        # average_scores[-1] += (0.1 * tree[move][0][i+1].points)
                        # 0.5 because we are dividing by the (number of children / 2),
                        # due to multiplying the number of point with the probability
                        # of having a 2 and a 4 per tile.
                    if len(tree[move][0]) > 0:
                        average_scores[-1] /= (len(tree[move][0]))
                    else:
                        average_scores[-1] = 0

                    # Determines best move
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
                if len(available_moves) == 1:
                    print(str(best_move[0] + "," + str(board1.board.flatten())))
                    file1 = open("exdata.txt", "a")

                    # Writes to training data text file
                    file1.write(str(best_move[0] + "," + str(board1.board.flatten().tolist())) + "\n")
                    file1.close()
                    board1.make_move(best_move[0])
                    break
                if depth == max_depth:
                    file1 = open("exdata.txt", "a")

                    # Writes to training data text file
                    file1.write(str(best_move[0] + "," + str(board1.board.flatten().tolist())) + "\n")
                    file1.close()
                    board1.make_move(best_move[0])


    cls()
    #beautify_print(board1.board)
    print("Final score: " + str(board1.points))
