import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import ast
from sklearn.metrics import plot_confusion_matrix, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pickle
from multiprocessing import cpu_count
cpus = cpu_count()
import tensorflow as tf
# config = tf.ConfigProto(device_count = {'GPU': 1, 'CPU': cpus}, log_device_placement=True)
# session = tf.Session(config)
# keras.backend.set_session(session)

le = LabelEncoder()

board = []
target = []

with open("../dataset.txt", "r") as file:
    for line in file.readlines():
        target.append(line[0])
        # board.append(np.array(ast.literal_eval(line[2:])).reshape(4, 4).tolist())
        board.append(ast.literal_eval(line[2:]))

train_data = pd.DataFrame(board)  
train_target = le.fit_transform(target)


X_train, X_test, y_train, y_test= train_test_split(train_data, train_target, test_size = 0.2, random_state = 0)
NUM_ONE_HOT_MAT = 16
WINDOW_LENGTH = 1
INPUT_SHAPE = (4, 4)
NUM_ACTIONS_OUTPUT_NN = 4 
INPUT_SHAPE_DNN = (WINDOW_LENGTH, 4+4*4, NUM_ONE_HOT_MAT,) + INPUT_SHAPE
model = Sequential()

# model.add(Flatten(input_shape=(4, 4)))
model.add(Dense(output_dim=16, activation='relu', input_dim=16))
# model.add(Dense(units=1024, activation='relu'))
# model.add(Dense(units=512, activation='relu'))
# model.add(Dense(units=256, activation='relu'))
# model.add(Dense(units=1, activation='linear'))
model.add(Dense(output_dim=16, activation='relu'))
model.add(Dense(output_dim=1, activation='linear'))
print(model.summary())

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, batch_size = 10, epochs = 100)

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(cm)

model.save_weights('./data/weights.h5f', overwrite=True)
pickle.dump(model, open('./data/keras_model.pkl', 'wb'), protocol=-1)
model.save('./data/keras_model.h5')