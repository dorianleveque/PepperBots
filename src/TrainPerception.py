import os
import cv2
import math
import random
import shutil
import time
import json
import numpy as np
import qibullet as qb
import pybullet as pb
import pybullet_data as pd

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split

"""def get2dPoint(point3D, viewMatrix, projectionMatrix, width, height):
    viewProjectionMatrix = np.multiply(projectionMatrix, viewMatrix)
    # transform world to clipping coordinates
    point3D = np.outer(viewProjectionMatrix,point3D).ravel()
    winX = round((( point3D[0] + 1 ) / 2.0) * width )
    # we calculate -point3D.getY() because the screen Y axis is
    # oriented top->down 
    winY = round((( 1 - point3D[1] ) / 2.0) * height )
    return [winX, winY]"""

def get2dPoint(point3D, viewMatrix, projectionMatrix, width, height):
    viewProjectionMatrix = np.multiply(projectionMatrix, viewMatrix)
    screenPos = np.outer(viewProjectionMatrix,point3D).ravel()
    screenPos = [((screenPos[0] + 1) / 2) * width, ((screenPos[1] + 1) / 2) * height, (screenPos[2] + 1) / 2]
    return [int(width - screenPos[0]), int(screenPos[1])]

class TrainPerception:
    """
    Class in charge of objet perception training of robot
    """

    def __init__(self, regenerate):
        self.datasetPath = "./build/images"
        self.modelPath = "./assets/models"

        if (regenerate or not os.path.isfile(self.modelPath + '/perception.h5')):
            self.generateDataset([
                ("empty", None, [0, 0, 1], 0),
                ("duck", "duck_vhacd.urdf", [0, 0, 1], 5),
                ("ball", "sphere2red.urdf", [0, 0, 1], 0.3),
                #("chair", "./assets/chair/chair.urdf", [0.5, -0.2, 0], 1),
                #("table", "./assets/table/table.urdf", [0, 0, 0], 1)
            ], 10)

    def generateDataset(self, objects, nbData):
        """
        Generate dataSet in build/images folder of workspace
        """
        classes = []
        # delete old dataset and create a new one
        shutil.rmtree(self.datasetPath)
        os.makedirs(self.datasetPath)

        # init simulation
        sim = qb.SimulationManager()
        client = sim.launchSimulation(gui=False)
        pb.setAdditionalSearchPath(pd.getDataPath())
        pb.loadURDF("plane.urdf")
        print('Data generation started.')

        for (label, model, position, scale) in objects:
            classes.append(label)

            # Define the "up" vector of the camear
            cameraUpVector = [0, 0, 1]

            # Create folder to save the images
            os.mkdir(self.datasetPath + '/' + str(label) + '/')

            m = pb.loadURDF(model, basePosition=position, globalScaling=scale) if (model != None) else None
            time.sleep(5)

            # Loop over various distances and angles
            for i in range(nbData):
                distance = random.uniform(0.5, 5)
                angle = random.uniform(0, 2*math.pi)
                height = random.uniform(1.10, 1.20)

                # Let the target be in the center, but not completely
                cameraTargetPosition = [random.uniform(-distance/2, distance/2),random.uniform(-distance/2, distance/2),random.uniform(0, 1)]

                # Vary the height of the eye (i.e. robot camera)
                cameraEyePosition = [distance * math.sin(angle), distance * math.cos(angle), height]

                # Compute view and projection matrices
                viewMatrix = pb.computeViewMatrix(cameraEyePosition, cameraTargetPosition, cameraUpVector)
                projectionMatrix = pb.computeProjectionMatrixFOV(57.20, 64/48, 0.01, 100)

                # Render and save the image
                width, height, rgbaImg, depthImg, segImg = pb.getCameraImage(width=64, height=48, viewMatrix=viewMatrix, projectionMatrix=projectionMatrix)
                #[x, y] = get2dPoint(cameraTargetPosition, viewMatrix, projectionMatrix, width, height)
                #x = x * (40 * 56) / width
                #y = y * (24 * 38) / height
                #w = (1/distance) * 10
                #h = (1/distance) * 10
                #print(x, y, w, h)

                save_path = self.datasetPath + '/' + str(label) + '/' + str(i) + '.png'
                rgbImg = rgbaImg[:, :, :3]  # remove the alpha channel
                cv2.imwrite(save_path, cv2.cvtColor(rgbImg, cv2.COLOR_RGB2BGR))

                # wait for a millisecond
                cv2.waitKey(1)

            print("> Generated " + str(nbData) + " '" + label + "' images")
            if (m != None):
                pb.removeBody(m)

        with open(self.modelPath + "/perception.class", 'w') as outfile:
            json.dump(sorted(classes), outfile)
        print("> Done!")

    def loadData(self):
        """
        Load the dataset generated in workspace
        """

        # Collect the classes
        classes = os.listdir(self.datasetPath)
        print('Found classes: ' + ', '.join(classes))

        # Count the total number of samples
        datasetLength = np.sum([len(next(os.walk(self.datasetPath + '/' + classe))[2]) for classe in classes])
        print('Found ' + str(datasetLength) + ' samples')

        # Construct the input and output arrays
        input = np.empty([datasetLength, 48, 64, 3])
        output = np.empty([datasetLength, len(classes)])

        # Load all the samples
        i = 0
        for classe in classes:
            for k in range(len(next(os.walk(self.datasetPath + '/' + classe))[2])):
                input[i] = cv2.imread(self.datasetPath + '/' + classe + '/' + str(k) + '.png')
                output[i] = np.zeros(len(classes))
                output[i][classes.index(classe)] = 1;
                i += 1

        return [input, output]

    def unison_shuffled_copies(self, a, b):
        """
        shuffle
        """
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    def train(self):
        """
        Train the model with the dataset previously generated
        """

        # Gather the inputs and outputs
        input, output = self.loadData()
        input, output = self.unison_shuffled_copies(input, output)

        # Split into training and validation, using 80/20 ratio
        split = round(0.8 * np.shape(input)[0])
        train_in, test_in = input[:split,:], input[split:,:]
        train_out, test_out = output[:split], output[split:]

        # Construct the model
        model = Sequential()
        model.add(Conv2D(4, input_shape=(48,64,3), strides=2, kernel_size=(3, 3), activation="relu", padding='same'))
        model.add(Conv2D(2, input_shape=(24,32,4), strides=2, kernel_size=(3, 3), activation="relu", padding='same'))
        model.add(Conv2D(1, input_shape=(12,16,2), strides=2, kernel_size=(3, 3), activation="relu", padding='same'))
        model.add(Flatten())
        model.add(Dense(32, activation='relu'))
        model.add(Dense(len(os.listdir(self.datasetPath)),  activation="softmax"))

        # Print the layer shapes to verify that the input shapes are correct
        for layer in model.layers:
            print(layer.output_shape)

        # Compile the network
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the network
        es_callback = EarlyStopping(monitor = "val_accuracy", patience = 10)
        model.fit(train_in, train_out,  validation_data=(test_in, test_out), epochs=10000, callbacks = [es_callback])

        # Since accuracy can be jumpy, make sure it is above 92% at least
        val_accuracy = 0;
        while val_accuracy < 0.90:
            results = model.fit(train_in, train_out,  validation_data=(test_in, test_out), epochs=1)
            val_accuracy = results.history['val_accuracy'][0]

        # Save the model
        model.save(self.modelPath + '/perception.h5')
        print("Perception model, successfully generated !")
