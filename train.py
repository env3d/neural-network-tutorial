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

numeric_classes = {
    'fas fa-battery-empty' : 0,
    'fas fa-bolt' : 1,
    'fas fa-check' : 2,
    'far fa-folder' : 3
}

#dataUrl = "https://ml-train-data.firebaseio.com/train.json";
dataUrl = "https://ml-train-data.firebaseio.com/train.json?orderBy=\"time\"&limitToFirst=180";

with urllib.request.urlopen(dataUrl) as json_data:
    d = list(json.load(json_data).values())

print('Training samples: '+str(len(d)));
target_vec = np.array([numeric_classes[x['clssification']] for x in d])

# we can convert to binary classification if we want
# target_vec = np.array([(1 if x == 0 else 0) for x in target_vec])

target_cat = keras.utils.to_categorical(target_vec, num_classes=4)

train_vec = np.array([x['imageData'] for x in d])

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
#              loss='binary_crossentropy',              
              metrics=['accuracy'])

model.fit(train_vec, target_cat, epochs=3, batch_size=1)
#model.save('my_icons.h5')
tfjs.converters.save_keras_model(model, 'my_icons.json')
print('finished training '+str(len(train_vec))+' datapoints')


