import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense
import ast
from ttictoc import TicToc
import pickle
from multiprocessing import cpu_count
from board import Board
from psutil import cpu_count
from multiprocessing import Pool
from reporting import beautify_print, plot_game_reports
from sklearn.preprocessing import StandardScaler
import click
import sys
from math import sqrt
cpus = cpu_count()

def one_hot_encode(row):
    for i, item in enumerate(row):
        if item > 0:
            row[i] = 1
    return row

def square_root_board(row):
    for i, item in enumerate(row):
        if item > 0:
            row[i] = sqrt(item)
    return row

def scale_data(row):
   return square_root_board(row)

# sys.exit()
@click.group()
def cli():
    pass

# =============================================================================
# Prepare data
# =============================================================================
moves_map = {
    'w': 0,
    'a': 1,
    's': 2,
    'd': 3
}

def prepare_y(direction):
    move = moves_map[direction]
    target_row = np.zeros(4)
    for i in range(len(target_row)):
        if i == move:
            target_row[i] = 1
    
    return np.array([target_row])

def load_and_transform_data(path = "dataset.txt"):
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
                    X_train = np.array([scale_data(ast.literal_eval(line[2:]))])
                    y_train = np.array(prepare_y(line[0]))
                    isFirstLine = False
                else:
                    X_train = np.append(X_train, [scale_data(ast.literal_eval(line[2:]))], axis=0)
                    y_train = np.append(y_train, prepare_y(line[0]), axis=0)
    except:
        pass
    pickle.dump((X_train, y_train), open('./data/transformed_dataset.pickle', 'wb'))
    scaler = StandardScaler()
    # return scaler.fit_transform(X_train), y_train
    return X_train, y_train
        
def load_transformed_data():
    return pickle.load(open('./data/transformed_dataset.pickle', 'r'))

# =============================================================================
# Train model
# =============================================================================

def train_model(X_train, y_train):    
    print('Training new model')
    model = Sequential()

    model.add(Dense(16, activation='relu', input_dim=16))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    print(model.summary())
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size = 100, epochs = 100)
    
    scores = model.evaluate(X_train, y_train, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
   
    # Save model
    model_json = model.to_json()
    with open("model/model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model/model.h5")
    print("Saved model to disk")
    return model  

# =============================================================================
# Play the game and predict moves
# =============================================================================

def get_move_by_value(move, moves_map):
    for key, value in moves_map.items():
        if move == value:
            return key

def play(original_board, model, print_board, color):
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
        if print_board == 'True':
            beautify_print(board1.board, color)  
        old_board = np.copy(board1.board)
        for i in range(1,5):
            board_to_predict = np.array([scale_data(board1.board.flatten())])
            # print('board to predict', board_to_predict)
            predicted_move = model.predict(board_to_predict)
            
            move_y = np.argsort(predicted_move[0])[-i]
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
    highest_tile = np.max(board1.board)
    didWin = highest_tile >= 2048
    return (moves, score, round(game_duration, 2), round(np.mean(np.array(move_time)), 2), didWin, highest_tile)

@cli.command('start')
@click.option('--print_board', default='False')
@click.option('--transform_dataset', default='False')
@click.option('--retrain_model', default='False')
@click.option('--color', default='True')
def start(print_board, transform_dataset, retrain_model, color):
# =============================================================================
# Load transformed dataset or transform the original one
# ============================================================================= 
    try:
        print('Trying to load transformed dataset')
        X_train, y_train = load_transformed_data() if transform_dataset == 'True' else load_and_transform_data()
        print('Transformed dataset loaded')
    except Exception:
        print('Could not load transformed data. Transforming original dataset')
        X_train, y_train = load_and_transform_data()
# =============================================================================
# Load Keras model or train a new one
# =============================================================================
    try:
        if retrain_model == 'True':
            model = train_model(X_train, y_train)
        else:
            print('Trying to load a model')
            json_file = open('model/model.json', 'r')
            loaded_model_json = json_file.read()
            model = model_from_json(loaded_model_json)
            model.load_weights('model/model.h5')    
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            print('Saved model loaded')
    except:
        model = train_model(X_train, y_train)
   
    n_games = 5
    output = []
    for i in range(0, n_games):
        board = Board()
        output.append(play(board, model, print_board, color))    
    plot_game_reports(output, save_csv = True, add_csv_suffix = False)

if __name__ == "__main__":
# =============================================================================
# To run this file from command line then comment out 'start()'
# To run this file from an IDE like Spyder then comment out 'cli()'
#
# If you have problems running the cli version you might want to use Anaconda prompt
# or make sure you have installed corect packages.
#
# *******
# cli args
#
# --print_board True|False
#
#   Specifies if the board should be printed while it is being played    
#    
# --transform_dataset True|False
# 
#   If set to False then cached transformed dataset will be loaded
#   Fallbacks to creating a new dataset
#
# --retrain_model True|False
#   
#   Specifies if the model should be compiled and fit with the dataset 
#   By default it will try to use a cached model and fallbacks to creating a new one
#
# --color True|False
#
#   For Window's CMD that do not work well with color printing. True turns it on,
#   False turns it off. Default is True.
#
#
# =============================================================================
    # cli()   
    start()
    pass
   
    
    
        
        