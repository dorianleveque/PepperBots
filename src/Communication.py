import os
import re
import json
import nltk
import numpy as np
import random
import pickle
from threading import Thread
from nltk.stem.lancaster import LancasterStemmer
# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

class Communication(Thread):

    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.model = tf.keras.models.load_model("./assets/models/communication.h5")
        self.indents = json.loads(open('./src/intents.json').read())
        self.words = pickle.load(open('./assets/models/words.pkl','rb'))
        self.labels = pickle.load(open('./assets/models/labels.pkl','rb'))
        self.stemmer = LancasterStemmer()

    def run(self):
        while True:
            userResponse = input("You: ")
            results = self.model.predict(np.array([self.bagOfWords(userResponse, self.words)]))
            self.say(self.getResponse(np.argmax(results), userResponse))

    def say(self, sentence):
        print("Pepper: ", sentence)

    def bagOfWords(self, s, words):
        bag = [0 for _ in range(len(words))]
        s_words = nltk.word_tokenize(s)
        s_words = [self.stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
                
        return (np.array(bag))

    def getPositionFromString(self, content):
        position = []
        matches = re.finditer(r"(-?\d+) (-?\d+)", content, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                position.append(int(match.group(groupNum)))
        return position

    def getResponse(self, topic, initialSentence):
        tag = self.labels[topic]
        if tag in ["Find_duck", "Find_ball"]:
            t = tag.split('_')
            if (len(t) == 2):
                self.robot.tasks.put(("find", t[1]))
            else:
                return "Sorry I don't understand."

        elif tag in ["Follow_duck", "Follow_ball"]:
            t = tag.split('_')
            if (len(t) == 2):
                self.robot.tasks.put(("follow", t[1]))
            else:
                return "Sorry I don't understand."

        elif tag in "MoveTo":
            position = self.getPositionFromString(initialSentence)
            if (len(position) == 2):
                self.robot.tasks.put(("moveTo", position))
            else:
                return "Sorry I don't understand."

        elif tag == "LookAt":
            position = self.getPositionFromString(initialSentence)
            if (len(position) == 2):
                self.robot.tasks.put(("lookAt", position))
            else:
                return "Sorry I don't understand."

        elif tag == "stop":
            self.robot.taskCanceled = True

        for tg in self.indents["intents"]:
            if tg['tag'] == tag:
                return random.choice(tg['responses'])

if __name__ == "__main__":
    com = Communication(None)
    com.start()