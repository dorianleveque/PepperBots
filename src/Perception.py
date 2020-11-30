import os
import cv2
import time
import math
import numpy as np
import qibullet as qb
from threading import Thread

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model

class Perception(Thread):

    def __init__(self, pepper):
        Thread.__init__(self)
        self.pepper = pepper
        self.classes = os.listdir('./build/images')
        self.model = load_model('./assets/models/perception.h5')
        self.classifications = []

        # Initialize front camera
        self.top_camera = self.pepper.subscribeCamera(qb.PepperVirtual.ID_CAMERA_TOP)

  
    def run(self):
        self.analyseEnvironment()

    def analyseEnvironment (self):
        # Retrieve and resize front image
        top_image = self.pepper.getCameraFrame(self.top_camera)
        cv2.imshow("top image", top_image)

        # Show the images
        top_image = cv2.resize(top_image, (64, 48))

        # predict
        test = np.zeros([1, 48, 64, 3])
        test[0,:] = top_image
        prediction = self.model(test, training=False)

        # Determine the object detected
        self.classifications.append(classes[np.argmax(prediction)])
        cv2.waitKey(1)