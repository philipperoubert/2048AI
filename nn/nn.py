import pandas as pd
import numpy as np
import keras
import random
from keras.models import Sequential
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

# config = tf.ConfigProto(device_count = {'GPU': 1, 'CPU': cpus}, log_device_placement=True)
# session = tf.Session(config)
# keras.backend.set_session(session)

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

with open("../dataset.txt", "r") as file:
    for line in file.readlines():
        target.append(line[0])
        # board.append(np.array(ast.literal_eval(line[2:])).reshape(4, 4).tolist())
        board.append(ast.literal_eval(line[2:]))

# train_data = pd.DataFrame(board)  

# train_target = le.fit_transform(target)
def prepare_train_data(data):
    return np.array(data).reshape(-1, len(data[0]), 1)
    # return np.array([np.array(row) for row in data]).reshape(-1, len(data[0]), 1)
        

def prepare_target_data(moves):
    target = []
    for key in moves:
        move = moves_map[key]
        target_row = np.zeros(4)
        for i in range(4):
            if i == move:
                target_row[i] = 1
        target.append(target_row)
    return target

train_data = prepare_train_data(board)
train_target = prepare_target_data(target)

X_train, X_test, y_train, y_test= train_test_split(train_data, train_target, test_size = 0.2, random_state = 0)

# =============================================================================
# Train model
# =============================================================================
# =============================================================================
# Tensorflow
# =============================================================================

def get_model(input_size):
    model = input_data(shape=[None, input_size, 1], name='input')
    model = fully_connected(model, 128, activation='relu')
    model = dropout(model, 0.8)
    model = fully_connected(model, 256, activation='relu')
    model = dropout(model, 0.8)
    model = fully_connected(model, 512, activation='relu')
    model = dropout(model, 0.8)
    model = fully_connected(model, 256, activation='relu')
    model = dropout(model, 0.8)
    model = fully_connected(model, 128, activation='relu')
    model = dropout(model, 0.8)
    model = fully_connected(model, 4, activation='softmax')
    model = regression(model, optimizer='adam', learning_rate=1e-3, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(model, tensorboard_dir='log')

    return model

model = get_model(input_size = len(X_train[0]))

model.fit({'input': X_train}, {'targets': y_train}, n_epoch=5 , snapshot_step=500, show_metric=True, run_id='2048AI')
model.save('data/tf.model')

# =============================================================================
# keras
# =============================================================================

def init_keras_model():
    model = Sequential()

    # model.add(Flatten(input_shape=(18975, 16, 1)))
    model.add(Dense(output_dim=16, activation='relu', input_shape=(16, 1)))
    model.add(Dense(units=1024, activation='relu'))
    model.add(Dense(units=512, activation='relu'))
    model.add(Dense(units=256, activation='relu'))
    model.add(Dense(16, activation='softmax'))
    print(model.summary())
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    model.fit(X_train, y_train, batch_size = 16, epochs = 100)
    y_pred = model.predict(y_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    model.save_weights('./data/weights.h5f', overwrite=True)
    pickle.dump(model, open('./data/keras_model.pkl', 'wb'), protocol=-1)
    model.save('./data/keras_model.h5')

# init_keras_model()


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
    t = TicToc()
      
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
        beautify_print(board1.board)        
        # Change from random.choice to use model prediction
        # Before board_state is provided it must be hot encoded
        # move_to_make = model.predict(board_state)
        move_prediction = random.choice(available_moves)
        move_to_make = get_move_by_value(move_prediction, moves_map)
        board1.make_move(move_to_make)
        moves[move_to_make] += 1
        # Get available moves for the next round
        available_moves = board1.moves_available(board1)
        # Add time duration of the move
        t.toc()
        move_time.append(t.elapsed)
    score = board1.points
    t.toc()
    game_duration = t.elapsed
    return (moves, score, game_duration, move_time)


if __name__ == "__main__":
    n_cpus = cpu_count()
    # print('n_cpus', n_cpus)
    # n_games = 5
    # board1 = Board()
    # board1.board = board1.board.astype(int)
    # pool = Pool(processes = n_cpus)
    # output = []
    # output = pool.map(play, [board1])
    # for i in range(0, 5):
    #     output.append(play(board1))
    # output = play()
    # print(output)

    
    
# =============================================================================
# Plot stats
# =============================================================================
# data = [(179, 1988, 0.4059131145477295), (117, 1172, 0.28848719596862793), (82, 592, 0.1765296459197998), (146, 1408, 0.49370384216308594), (69, 412, 0.17749881744384766)]
    # plot_game_reports(data)
   
    
    
        
        