# ANN RPS Bot
name = 'ann_bot'

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np
import random
import trutheyfalseybot as tfb

ohe_encodings = {'R':0, 'P':1, 'S':2}
reverse_encodings = {ohe_encodings[move]:move for move in ohe_encodings}
lose_against_map = {'S':'R', 'R':'P', 'P':'S'}

def process_ann_data(opp_hist, my_hist):
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

def process_rnn_data(opp_hist, seq_length):
    n_seqs = len(opp_hist)-seq_length
    x = np.zeros((n_seqs, seq_length, 3))
    y = np.zeros((n_seqs, 3))
    for i in range(n_seqs):
        for j in range(seq_length):
            x[i][j][ohe_encodings[opp_hist[i+j][1]]] = 1
        y[i][ohe_encodings[opp_hist[i+seq_length][1]]] = 1
    return x,y

def fit_ann(model, opp_hist, my_hist, init_epoch, n_epochs):
    x, y = process_ann_data(opp_hist, my_hist)
    model.fit(x, y, batch_size=4, initial_epoch=init_epoch, epochs=n_epochs, verbose=0)
    
def fit_rnn(model, opp_hist, init_epoch, n_epochs):
    x, y = process_rnn_data(opp_hist, 8)
    model.fit(x, y, batch_size=4, initial_epoch=init_epoch, epochs=n_epochs, verbose=0)

class RPSBot(object):
    name = name
    def __init__(self):
        self.init_model()
        self.bot = tfb.RPSBot()
        
    def init_model(self):
        self.ann = Sequential()
        self.ann.add(Dense(input_dim=6, units=4, activation='relu'))
        self.ann.add(Dense(units=4, activation='relu'))
        self.ann.add(Dense(units=3, activation='softmax'))
        self.ann.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        self.rnn = Sequential()
        self.rnn.add(LSTM(units=5, input_shape=(8, 3)))
        self.rnn.add(Dense(units=3, activation='softmax'))
        self.rnn.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        
        self.epoch = 0
        self.epochs_per_train = 1     
        
    def get_hint(self, opp_hist, my_hist):
        if len(opp_hist) > 75:
            fit_ann(self.ann, opp_hist, my_hist, self.epoch, self.epoch+self.epochs_per_train)
            fit_rnn(self.rnn, opp_hist, self.epoch, self.epoch+self.epochs_per_train)
            self.epoch += self.epochs_per_train
            x = np.zeros((1,8,3))
            for i in range(8):
                index = i-8
                x[0,i,ohe_encodings[opp_hist[index][1]]] = 1
            y = self.rnn.predict(x)[0]
            index = np.argmax(y)
            pred_move = reverse_encodings[index]
            return lose_against_map[pred_move]
        elif len(opp_hist) == 0:
            self.init_model()
        return random.choice('RPS')
    
    def get_move(self, opp_hist, my_hist, opp_hint, my_hint):
        if len(opp_hist) > 125:
            x = np.zeros((1,6))
            x[0,ohe_encodings[opp_hint]] = 1
            x[0,3+ohe_encodings[my_hint]] = 1
            y = self.ann.predict(x)[0]
            index = np.argmax(y)
            pred_move = reverse_encodings[index]
            return lose_against_map[pred_move]
        return self.bot.get_move(opp_hist, my_hist, opp_hint, my_hint)