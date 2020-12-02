import json
import random
import os
import nltk
import numpy as np
import pickle
from nltk.stem.lancaster import LancasterStemmer

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.models import Sequential

def make_chatbot_learning():
    # ==== Preparation ====
    stemmer = LancasterStemmer()

    with open('./src/intents.json') as file:
        data = json.load(file)

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    # ==== Word stemming (find the root of the word) ====
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    pickle.dump(words,open('./assets/models/words.pkl','wb'))
    pickle.dump(labels,open('./assets/models/labels.pkl','wb'))

    # ==== Bag of words ====
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)

    # Converting training data into numpy arrays
    training = np.array(training)
    output = np.array(output)

    # ==== Developping a model ====
    model = Sequential()
    model.add(Dense(128, input_shape=(len(training[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(output[0]), activation='softmax'))

    # ==== Training and saving of the model ====
    #sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    #fitting and saving the model
    model.fit(np.array(training), np.array(output), epochs=1000, batch_size=8, verbose=1)
    model.save('./assets/models/communication.h5')

if __name__ == "__main__":
    make_chatbot_learning()