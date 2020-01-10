from monte_carlo_board import Board
import os
from termcolor import colored
import numpy as np
import random
from multiprocessing import Pool

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

def cls():
    """
    Clears the console (used to make it prettier, not needed in reality)
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def simulate_run(board):
    newer_board = Board(board.board, board.points)
    first_iteration = True
    
    first_move = None
    while newer_board.moves_available():
        available_moves = newer_board.moves_available(True)  # Gets a list of all possible moves
        move_to_make = random.choice(available_moves)
        newer_board.make_move(move_to_make)
        if first_iteration:
            first_move = move_to_make
            first_iteration = False
    return [first_move, newer_board.points]

if __name__ == "__main__":

    for _ in range(5):

        board1 = Board()  # Initialise a board
        number_of_processors = 4 # For multiprocessing
        board1.board = board1.board.astype(int)
        cls()  # using clear function here as it seems that not using it would corrupt the output

        print("Board initialised:")
        beautify_print(board1.board)
        moves = 0

        while board1.moves_available():
            cls() # comment this out if you want the program to print out everything
            beautify_print(board1.board)
            depth = 1 # number of games being played
            final_scores = {"w":[0,0], "a":[0,0], "s":[0,0], "d":[0,0],}

            with Pool(number_of_processors) as p:
                scores = p.map(simulate_run, [board1] * depth)
            print('scores', scores)
            for score in scores:
                final_scores[score[0]][0] += score[1]
                final_scores[score[0]][1] += 1

            best_score = 0
            for i in final_scores:
                try:
                    final_scores[i][0] /= final_scores[i][1]
                except:
                    final_scores[i][0] = 0
                if final_scores[i][0] > best_score:
                    best_score = final_scores[i][0]
                    best_move = i

            with open("dataset.txt", "a") as file:
                file.write(str(best_move + "," + str(list(board1.board.flatten())) + "\n"))
            file.close()
            board1.make_move(best_move)
            moves += 1

        cls()
        beautify_print(board1.board)
        print("Final Score: " + str(board1.points))
        print("Moves: " + str(moves))
