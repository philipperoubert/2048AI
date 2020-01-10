from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.optimizers import SGD, Adam
from monte_carlo_board import Board
from game_helpers import beautify_print
import numpy as np
import ast
import os

def cls():
    """
    Clears the console (used to make it prettier, not needed in reality)
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def translateYtoMove(y):
    if y == 0:
        return "w"
    elif y == 1:
        return "a"
    elif y == 2:
        return "s"
    else:
        return "d"


def translateMoveToY(move):
    if move == "w":
        Y = np.array([[1,0,0,0]])
    elif move == "a":
        Y = np.array([[0,1,0,0]])
    elif move == "s":
        Y = np.array([[0,0,1,0]])
    else:
        Y = np.array([[0,0,0,1]])
    return Y

def makeXY():
    first_line = True
    with open("dataset.txt", "r") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            if first_line:
                X = np.array([ast.literal_eval(line[2:])])
                Y = np.array(translateMoveToY(line[0]))
                first_line = False
            else:
                X = np.append(X, [ast.literal_eval(line[2:])], axis = 0)
                Y = np.append(Y, translateMoveToY(line[0]), axis = 0)
            if X.shape[0] % 10000 == 0:
                print(X.shape, Y.shape)
    return X, Y







X, Y = makeXY()
print(X.shape, Y.shape)

model = Sequential()
model.add(Dense(16, input_dim=16))
model.add(Dense(16))
model.add(Dense(4))

sgd = SGD(lr=0.01, momentum=0.9,  nesterov=True)
adam = Adam()
model.compile(loss='categorical_crossentropy', optimizer=sgd)
model.fit(X, Y, batch_size=100, epochs=10)

board1 = Board()
while board1.moves_available():
    old_board = np.copy(board1.board)
    for i in range(1,5):
        move_y = np.argsort(model.predict(np.array([board1.board.flatten()]))[0])[-i]
        board1.make_move(translateYtoMove(move_y))
        if not np.array_equal(board1.board, old_board):
            break
    cls()
    beautify_print(board1.board)
