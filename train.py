# Must have keras and the associate dependencies installed
# developed on python 3.6

import numpy as np
import json
import urllib.request

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

import tensorflowjs as tfjs

import os
import sys


def get_data(data_points = None):

    if data_points == None:
        dataUrl = "https://ml-train-data.firebaseio.com/train.json";
    else:
        dataUrl = f"https://ml-train-data.firebaseio.com/train.json?orderBy=\"time\"&limitToFirst={data_points}";

    with urllib.request.urlopen(dataUrl) as json_data:
        d = list(json.load(json_data).values())

    numeric_classes = {
        'fas fa-battery-empty' : 0,
        'fas fa-bolt' : 1,
        'fas fa-check' : 2,
        'far fa-folder' : 3
    }
    
    # conver the data to numbers
    target_vec = np.array([numeric_classes[x['clssification']] for x in d])
    
    # we can convert to binary classification if we want
    # target_vec = np.array([(1 if x == 0 else 0) for x in target_vec])

    # now we need to output the categories    
    target_cat = keras.utils.to_categorical(target_vec, num_classes=4)
    train_vec = np.array([x['imageData'] for x in d])
    
    return train_vec, target_cat
    

def train(num_data_points = None, epochs = 3, batch_size = 1):

    train_vec, target_cat = get_data(data_points = num_data_points)
    
    print(f"Number of training samples: {len(train_vec)}");
    print(f"Epochs = {epochs}, Batch Size = {batch_size}");
    
    # create the model
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    #model.add(Activation('sigmoid'))
    #model.add(Activation('softmax'))
    model.add(Dense(4))
    #model.add(Activation('sigmoid'))
    model.add(Activation('softmax'))

    opt = 'rmsprop'

    model.compile(optimizer=opt,
                  loss='categorical_crossentropy',
                  # loss='binary_crossentropy',              
                  metrics=['accuracy'])

    # train the model 
    model.fit(train_vec, target_cat, epochs=epochs, batch_size=batch_size)

    # optionally save the model in keras format
    # model.save('my_icons.h5')

    # save the model in tensorflowjs format for use in web
    tfjs.converters.save_keras_model(model, 'my_icons.json')
    
    print('finished training '+str(len(train_vec))+' datapoints')

if __name__ == "__main__":
    train()
