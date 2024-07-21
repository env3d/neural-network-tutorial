# Must have keras and the associate dependencies installed
# developed on python 3.6

import numpy as np
import json
import urllib.request
import datetime

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

import tensorflowjs as tfjs

import psycopg
import db

def get_data(last_x_minutes=60):
    with psycopg.connect(**db.params) as conn:
        with conn.cursor() as cursor:
            print("Connected to the database.")

            current_time = datetime.datetime.now()
            tail_time = datetime.timedelta(minutes=last_x_minutes)
            query_time = current_time - tail_time

            select_query = f"""SELECT data FROM training_data WHERE timestamp 
            > '{query_time.strftime('%Y-%m-%d %H:%M:%S')}'"""
            cursor.execute(select_query)

            # Fetch and print results
            results = cursor.fetchall()
            d = [ r[0] for r in results ]

            print(f"Number of training samples: {len(d)}")

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
        

def get_data_firebase(date = None, days = 1):

    if date == None:
        # default to the original training set
        params = "?orderBy=\"time\"&limitToFirst=187"
    else:        
        time = datetime.datetime.fromordinal(date.toordinal())
        timedelta = datetime.timedelta(days = days)        
        startAt = int(time.timestamp() * 1000)
        endAt = int( (time+timedelta).timestamp() * 1000)
        params = f"?orderBy=\"time\"&startAt={startAt}&endAt={endAt}"
    
    dataUrl = f"https://ml-train-data.firebaseio.com/train.json{params}"

    print(dataUrl)
    
    with urllib.request.urlopen(dataUrl) as json_data:
        d = list(json.load(json_data).values())

    print(f"Number of training samples: {len(d)}")
    
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
    
def train(train_vec, target_cat, epochs = 3, batch_size = 1):
    
    print(f"Epochs = {epochs}, Batch Size = {batch_size}")

    if len(train_vec) < 10:
        print("Not enough sample to train")
        return
    
    # create the model
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu')) # other common options are 'sigmod' and 'softmax'
    model.add(Dense(4))
    model.add(Activation('softmax')) # 'softmax' gives us percentages

    opt = 'rmsprop'

    model.compile(optimizer=opt,
                  loss='categorical_crossentropy', # 'binary_crossentrpoy' for binary classification
                  metrics=['accuracy'])

    # train the model 
    model.fit(train_vec, target_cat, epochs=epochs, batch_size=batch_size)

    # optionally save the model in keras format
    # model.save('my_icons.h5')

    # save the model in tensorflowjs format for use in web
    tfjs.converters.save_keras_model(model, 'my_icons.json')
    
    print('finished training '+str(len(train_vec))+' datapoints')

def train_today():
    # train on today's data
    train(*get_data(last_x_minutes=1440))
    
#if __name__ == '__main__':
#    train_original()
