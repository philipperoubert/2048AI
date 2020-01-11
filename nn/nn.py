import pandas as pd
import numpy as np
import keras
import random
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical
import ast
from sklearn.metrics import plot_confusion_matrix, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from ttictoc import TicToc
import pickle
from multiprocessing import cpu_count
cpus = cpu_count()
import tensorflow as tf
from monte_carlo_board import Board
from psutil import cpu_count
from multiprocessing import Pool
from game_helpers import beautify_print, get_scores, plot_game_reports, plot_table
import matplotlib.pyplot as plt

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

le = LabelEncoder()

# =============================================================================
# Prepare data
# =============================================================================
moves_map = {
    'w': 0,
    'a': 1,
    's': 2,
    'd': 3
}

board = []
target = []

def prepare_y(direction):
    move = moves_map[direction]
    target_row = np.zeros(4)
    for i in range(len(target_row)):
        if i == move:
            target_row[i] = 1
    
    return np.array([target_row])

def load_and_transform_data(path = "../dataset.txt"):
    isFirstLine = True
    try:
        with open(path, "r") as file:        
            for line in file.readlines():
                # Skip an empty line
                if len(line) == 0:
                    continue
                
                # Remove break line
                line = line.replace("\n", "")
                
                # On the first 
                if isFirstLine:
                    X_train = np.array([ast.literal_eval(line[2:])])
                    y_train = np.array(prepare_y(line[0]))
                    isFirstLine = False
                else:
                    X_train = np.append(X_train, [ast.literal_eval(line[2:])], axis=0)
                    y_train = np.append(y_train, prepare_y(line[0]), axis=0)
    except Exception as e:
        print('exception', e)
    pickle.dump((X_train, y_train), open('./data/transformed_dataset.pickle', 'wb'))
    return X_train, y_train
        
def load_transformed_data():
    pickle.load(open('./data/transformed_dataset.pickle', 'r'))

# =============================================================================
# Load transformed dataset or transform the original one
# =============================================================================
    
try:
    print('Trying to load transformed dataset')
    X_train, y_train = load_transformed_data()
    print('Transformed dataset loaded')
except Exception:
    print('Could not load transformed data. Transforming original dataset')
    X_train, y_train = load_and_transform_data()

# X_train, X_test, y_train, y_test= train_test_split(X_train, y_train, test_size = 0.2, random_state = 0)

# =============================================================================
# Train model
# =============================================================================

def train_model(X_train, y_train):
    model = Sequential()

    model.add(Dense(16, activation='relu', input_dim=16))
    # model.add(Dense(16))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(4))
    print(model.summary())
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size = 100, epochs = 100)
    
    scores = model.evaluate(X_train, y_train, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
   
    # Save model
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")
    print("Saved model to disk")
    return model  

try:
    print('Trying to load a model')
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)
    model.load_weights('model.h5')    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print('Saved model loaded')
except:
    print('Training new model')
    model = train_model(X_train, y_train)


# =============================================================================
# Play the game and predict moves
# =============================================================================

def get_move_by_value(move, moves_map):
    for key, value in moves_map.items():
        if move == value:
            return key

def play(original_board, model):
    # Initialise the board
    board1 = Board(original_board.board, original_board.points)
    
    # Start game timer
    t_game = TicToc()
    t = TicToc()
    t_game.tic()
    # Dict for counting each move
    moves = {
        'w': 0,
        'a': 0,
        's': 0,
        'd': 0
    }
    
    # Get initial available moves
    available_moves = board1.moves_available(board1)
    
    move_time = []
    # Play the game as long as we have available moves
    while available_moves:
        t.tic()  
        # beautify_print(board1.board)  
        old_board = np.copy(board1.board)
        for i in range(1,5):
            predicted_move = model.predict(np.array([board1.board.flatten()]))
            # print('predicted_move', predicted_move)
            move_y = np.argsort(predicted_move[0])[-i]
            # print('move_y', move_y, np.argsort(predicted_move[0]))
            predicted_move_key = get_move_by_value(move_y, moves_map)
            board1.make_move(predicted_move_key)
            moves[predicted_move_key] += 1
            if not np.array_equal(board1.board, old_board):
                break
      
        
        # Get available moves for the next round
        available_moves = board1.moves_available(board1)
        # Add time duration of the move
        t.toc()
        move_time.append(t.elapsed)
    score = board1.points
    t_game.toc()
    game_duration = t_game.elapsed
    didWin = np.max(board1.board) >= 2048
    return (moves, score, round(game_duration, 2), round(np.mean(np.array(move_time)), 2), didWin)


if __name__ == "__main__":
    n_cpus = cpu_count()
    # print('n_cpus', n_cpus)
    n_games = 5
   
    # board1.board = board1.board.astype(int)
    # pool = Pool(processes = n_cpus)
    output = []
    # output = pool.map(play, [board1])
    for i in range(0, n_games):
        board = Board()
        output.append(play(board, model))
    # output = play(board, model)
    print(output)
    
    plot_game_reports(output)
   
    
    
        
        