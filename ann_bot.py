# ANN RPS Bot
name = 'ann_bot'

from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import random

ohe_encodings = {'R':0, 'P':1, 'S':2}
reverse_encodings = {ohe_encodings[move]:move for move in ohe_encodings}
lose_against_map = {'S':'R', 'R':'P', 'P':'S'}

def process_data(opp_hist, my_hist):
    x = np.zeros((len(opp_hist), 6))
    y = np.zeros((len(my_hist), 3))
    for i in range(len(opp_hist)):
        opp_hint = opp_hist[i][0]
        my_hint = my_hist[i][0]
        opp_move = opp_hist[i][1]
        x[i,ohe_encodings[opp_hint]] = 1
        x[i,3+ohe_encodings[my_hint]] = 1
        y[i,ohe_encodings[opp_move]] = 1
    return x, y

def fit(model, opp_hist, my_hist, init_epoch, n_epochs):
    x, y = process_data(opp_hist, my_hist)
    model.fit(x, y, batch_size=4, initial_epoch=init_epoch, epochs=n_epochs, verbose=1)

class RPSBot(object):
    name = name
    def __init__(self):
        self.init_model()
        
    def init_model(self):
        self.model = Sequential()
        self.model.add(Dense(input_dim=6, units=4, activation='relu'))
        self.model.add(Dense(units=4, activation='relu'))
        self.model.add(Dense(units=3, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.epoch = 0
        self.epochs_per_train = 1     
        
    def get_hint(self, opp_hist, my_hist):
        if len(opp_hist) > 5:
            fit(self.model, opp_hist, my_hist, self.epoch, self.epoch+self.epochs_per_train)
            self.epoch += self.epochs_per_train
        elif len(opp_hist) == 0:
            self.init_model()
        return random.choice('RPS')
    
    def get_move(self, opp_hist, my_hist, opp_hint, my_hint):
        x = np.zeros((1,6))
        x[0,ohe_encodings[opp_hint]] = 1
        x[0,3+ohe_encodings[my_hint]] = 1
        y = self.model.predict(x)[0]
        index = np.argmax(y)
        pred_move = reverse_encodings[index]
        return lose_against_map[pred_move]