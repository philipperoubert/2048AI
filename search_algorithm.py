from board import Board
import os
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


def find_children(board, is_initial=False):
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
            for two_four in [2, 4]:
                spawned_board = Board(parent.board, parent.points)
                spawned_board.spawn_number(pick_random=False, rand=cell_index, spawn_number=two_four)
                children.append(spawned_board)
                del spawned_board
    return children



if __name__ == "__main__":

    board1 = Board()

    cls()

    print("Board initialised:")

    while board1.moves_available:
        beautify_print(board1.board)
        depth = 0
        tree = {"w": [[],[]], "a":[[],[]], "s":[[],[]], "d":[[],[]]} # [[parents][children]]
        available_moves = board1.moves_available(True)
        while depth < 3:
            if depth == 0:
                for move in available_moves:
                    moved_board = Board(board1.board, board1.points)
                    moved_board.make_move(move, False)
                    tree[move][0] += find_children(board=moved_board, is_initial=True)
                    del moved_board
                depth += 1
            else:
                print(available_moves)
                for move in available_moves:
                    for parent in tree[move][0]:
                        tree[move][1] += find_children(board=parent)
                depth += 1
                average_scores = []
                for move in available_moves:
                    tree[move][0] = tree[move][1]
                    tree[move][1] = []
                    average_scores.append(0)
                    for i in range(0, len(tree[move][0]), 2):
                        average_scores[-1] += (0.9 * tree[move][0][i].points)
                        average_scores[-1] += (0.1 * tree[move][0][i+1].points)
                    average_scores[-1] /= (0.5 * len(tree[move][0]))
                    print("Move " + move + " has an average " +  str(average_scores[-1]) + " at depth " + str(depth))

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
                for move in compare_moves:
                    if move not in best_move:
                        tree[move][0] = []
                        available_moves.remove(move)
                print("Possible moves:")
                print(available_moves)
                if len(available_moves) == 1:
                    board1.make_move(best_move[0])
                    break
                if depth == 6:
                    board1.make_move(best_move[0])
