import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Activation, Dense, LSTM
import os
import random


filepath = tf.keras.utils.get_file('poems.txt','r')
text = open(filepath, 'rb').read().decode(encoding='utf-8').lower()
text = text[100:2500000]
characters = sorted(set(text))
estimateChar = dict((c, i) for i, c in enumerate(characters))
estimateIndex = dict((i, c) for i, c in enumerate(characters))
line = []
nextChar = []

# Number of characters used before generating random text
SEQ_LENGTH = 10
STEP_SIZE = 3


# Differenciating characters and estimating the best suitable outcome
for i in range(0, len(text) - SEQ_LENGTH, STEP_SIZE):
    line.append(text[i: i + SEQ_LENGTH])
    nextChar.append(text[i + SEQ_LENGTH])

x = np.zeros((len(line), SEQ_LENGTH,len(characters)), dtype=np.bool)
y = np.zeros((len(line),len(characters)), dtype=np.bool)

for i, sent in enumerate(line):
    for j, char in enumerate(sent):
        x[i, j, estimateChar[char]] = 1
    y[i, estimateChar[nextChar[i]]] = 1


# Training the model
model = Sequential()
model.add(LSTM(128,input_shape=(SEQ_LENGTH,len(characters))))
model.add(Dense(len(characters)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy',optimizer=RMSprop(lr=0.01))
model.fit(x, y, batch_size=256, epochs=27)


# Depending on temp, text is being generated with different sufficiency rates
def sampleModel(preds, temp=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temp
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# Generating text from the trained model
def generateText(length, temp):
    firstIndex = random.randint(0, len(text) - SEQ_LENGTH - 1)
    outcome = ''
    poeticText = text[firstIndex: firstIndex + SEQ_LENGTH]
    outcome += poeticText

    
    for i in range(length):
        x = np.zeros((1, SEQ_LENGTH, len(characters)))
        for j, character in enumerate(poeticText):
            x[0, j, estimateChar[character]] = 1

        prediction = model.predict(x, verbose=0)[0]
        secondIndex = sampleModel(prediction, temp)
        assignedIndex = estimateIndex[secondIndex]
        outcome += assignedIndex
        poeticText = poeticText[1:] + assignedIndex
    
    return outcome



 




    
