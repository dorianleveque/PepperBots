import os
import cv2
import math
import random
import shutil
import time
import numpy as np
import qibullet as qb
import pybullet as pb
import pybullet_data as pd

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.models import Sequential


class TrainPerception:

    def __init__(self):
        self.datasetPath = "./build/images"
        self.generateDataset([
            ("empty", "", 0),
            ("duck", "duck_vhacd.urdf", 5),
            ("ball", "shere2red.urdf", 0.3),
            ("chair", "./assets/chair/chair.urdf", 5),
            ("table", "./assets/table/table.urdf", 5)
        ], 3000)

    def generateDataset(self, objects, nbData):
        # delete old dataset and create a new one
        shutil.rmtree(self.datasetPath)
        os.makedirs(self.datasetPath)

        # init simulation
        sim = qb.SimulationManager()
        client = sim.launchSimulation(gui=False)
        pb.setAdditionalSearchPath(pd.getDataPath())
        print('Data generation started.')

        for (label, model, scale) in objects:
            # Define the "up" vector of the camear
            cameraUpVector = [0, 0, 1]

            # Create folder to save the images
            os.mkdir(self.datasetPath + '/' + str(label) + '/')

            m = pb.loadURDF("sphere2red.urdf", basePosition=[
                            0, 0, 1], globalScaling=scale)
            time.sleep(3)

            # Loop over various distances and angles
            for i in range(nbData):
                distance = random.uniform(0.5, 5)
                angle = random.uniform(0, 2*math.pi)
                height = random.uniform(1.10, 1.20)

                # Let the target be in the center, but not completely
                cameraTargetPosition = [
                    random.uniform(-distance/2, distance/2),
                    random.uniform(-distance/2, distance/2),
                    random.uniform(0, 1)
                ]

                # Vary the height of the eye (i.e. robot camera)
                cameraEyePosition = [
                    distance * math.sin(angle),
                    distance * math.cos(angle),
                    height
                ]

                # Compute view and projection matrices
                viewMatrix = pb.computeViewMatrix(
                    cameraEyePosition, cameraTargetPosition, cameraUpVector)
                projectionMatrix = pb.computeProjectionMatrixFOV(
                    57.20, 64/48, 0.01, 100)

                # Render and save the image
                width, height, rgbaImg, depthImg, segImg = pb.getCameraImage(
                    width=64, height=48, viewMatrix=viewMatrix, projectionMatrix=projectionMatrix)
                save_path = self.datasetPath + '/' + \
                    str(label) + '/' + str(i) + '.png'
                rgbImg = rgbaImg[:, :, :3]  # remove the alpha channel
                cv2.imwrite(save_path, cv2.cvtColor(rgbImg, cv2.COLOR_RGB2BGR))

                # wait for a millisecond
                cv2.waitKey(1)

            print("> Generated '" + label + "' images")
            pb.removeBody(m)

        print("> Done!")

    def loadData(self):
        # Collect the classes
        classes = os.listdir(self.datasetPath)
        print('Found three classes: ' + ', '.join(classes))

        # Count the total number of samples
        datasetLength = np.sum(
            [len(next(os.walk(self.datasetPath + '/' + classe))[2]) for classe in classes])
        print('Found ' + str(datasetLength) + ' samples')

        # Construct the input and output arrays
        input = np.empty([datasetLength, 48, 64, 3])
        output = np.empty([datasetLength])

        # Load all the samples
        i = 0
        for classe in classes:
            for k in range(len(next(os.walk(self.datasetPath + '/' + classe))[2])):
                input[i] = cv2.imread(
                    self.datasetPath + '/' + classe + '/' + str(k) + '.png')
                output[i] = classe  # np.zeros(len(classes))
                #output[i][j] = 1;
                i += 1

        return [input, output]

    def train(self):
        # Gather the inputs and outputs
        input, output = self.loadData()
        input, output = unison_shuffled_copies(input, output)
        print(np.shape(input))
        print(np.shape(output))

        """# Split into training and validation, using 80/20 ratio
        split = round(0.8 * np.shape(input)[0])
        train_in, val_in = input[:split,:], input[split:,:]
        train_out, val_out = output[:split], output[split:]

        # Construct the model
        model = Sequential()
        model.add(Conv2D(4, input_shape=(48,64,3), strides=2, kernel_size=(3, 3), activation="relu", padding='same'))
        model.add(Conv2D(2, input_shape=(24,32,4), strides=2, kernel_size=(3, 3), activation="relu", padding='same'))
        model.add(Conv2D(1, input_shape=(12,16,2), strides=2, kernel_size=(3, 3), activation="relu", padding='same'))
        model.add(Flatten())
        model.add(Dense(32, activation='relu'))
        model.add(Dense(len(os.listdir('./images')),  activation="softmax"))

        # Print the layer shapes to verify that the input shapes are correct
        for layer in model.layers:
            print(layer.output_shape)

        # Compile the network
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the network
        es_callback = EarlyStopping(monitor = "val_accuracy", patience = 10)
        model.fit(train_in, train_out,  validation_data=(val_in, val_out), epochs=10000, callbacks = [es_callback])

        # Since accuracy can be jumpy, make sure it is above 92% at least
        val_accuracy = 0;
        while val_accuracy < 0.90:
            results = model.fit(train_in, train_out,  validation_data=(val_in, val_out), epochs=1)
            val_accuracy = results.history['val_accuracy'][0]

        # Save the model
        model.save('./model/my_model.h5')"""
