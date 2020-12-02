import json
import nltk
import numpy
import random
import tensorflow
import tflearn
from nltk.stem.lancaster import LancasterStemmer

pathOfModel = "models/model.tflearn" # A modifier si besoin



def retrieve_config_DNN(): # nb neurons (begin,end)
    with open("models/configDNN.txt","r") as fichier: # Le fichier doit exister
        texte = fichier.read()
    texte_split = texte.split("\n")
    return int(texte_split[0]), int(texte_split[1])


stemmer = LancasterStemmer()
tensorflow.compat.v1.reset_default_graph()

# Configuration du DNN
nbEntree, nbSortie = retrieve_config_DNN()
net = tflearn.input_data(shape=[None, nbEntree])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, nbSortie, activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net) # Creation de reseau de neurones profond
model.load(pathOfModel)


# Recup des mots
with open('intents.json') as file:
    data = json.load(file)
words = []
labels = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
# ==== Word stemming (find the root of the word) ====
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))
labels = sorted(labels)



def find_the_duck():
    print("Duck searching fonction. TODO")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat(trained_model):
    print("Start talking with the bot (type quit to stop) !")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = trained_model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        if tag == "duck":
            find_the_duck()
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        print("Pepper: ",random.choice(responses))

if __name__ == "__main__":
    chat(model)