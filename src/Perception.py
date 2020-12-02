import os
import cv2
import time
import math
import json
import imutils
import numpy as np
import qibullet as qb
from threading import Thread
from multiprocessing.pool import ThreadPool

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

class LoadPerceptionModelError(Exception):
    """Perception model isn't generated. You need to generate model before."""
    pass

def sliding_window(image, step, ws):
	# slide a window across the image
	for y in range(0, image.shape[0] - ws[1], step):
		for x in range(0, image.shape[1] - ws[0], step):
			# yield the current window
			yield (x, y, image[y:y + ws[1], x:x + ws[0]])

def image_pyramid(image, scale=1.5, minSize=(40, 40)):
	# yield the original image
	yield image

	# keep looping over the image pyramid
	while True:
		# compute the dimensions of the next image in the pyramid
		w = int(image.shape[1] / scale)
		image = imutils.resize(image, width=w)

		# if the resized image does not meet the supplied minimum
		# size, then stop constructing the pyramid
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			break

		# yield the next image in the pyramid
		yield image

class Perception(Thread):

    def __init__(self, pepper):
        Thread.__init__(self)
        self.pepper = pepper

        # import perception model
        if os.path.isfile('./assets/models/perception.class') and os.path.isfile('./assets/models/perception.h5'):
            with open('./assets/models/perception.class') as content:
                self.classes = json.load(content)
            tf.compat.v1.disable_eager_execution()
            self.model = tf.keras.models.load_model('./assets/models/perception.h5')
        else:
            raise LoadPerceptionModelError

        # Do a single null prediction to speed up model
        test = np.zeros([1, 48, 64, 3])
        self.model.predict(test)[0]

        # Initialize front camera
        self.handle = self.pepper.subscribeCamera(qb.PepperVirtual.ID_CAMERA_TOP)

    def run(self):
        """pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.find, (image, self.targetName))
        boundingBox = async_result.get()"""
        while True:
            image = self.getScreenShotFromCamera()
            self.display("Top Camera", image)


    def display(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(1)

    def getScreenShotFromCamera(self):
        return self.pepper.getCameraFrame(self.handle)

    def find(self, targetName):
        image = self.getScreenShotFromCamera()
        classifications = []

        # 3 predictions
        for i in range(3):
            test = np.zeros([1, 48, 64, 3])
            test[0,:] = cv2.resize(image, (64, 48))
            prediction = self.model(test, training=False)
            index = np.argmax(prediction)
            classifications.append(self.classes[index])

        # Determine the object that is in front
        mostFrequent = max(set(classifications), key=classifications.count)
        print(classifications, mostFrequent, targetName)
        return mostFrequent == targetName
        #return prediction[self.classes.index(targetName)] > 0.95

    def findLocationInScreen(self, targetName):
        if (targetName != None):
            image = self.getScreenShotFromCamera()
            #pool = ThreadPool(processes=1)
            #async_result = pool.apply_async(self.getBoundingBox, (image, targetName)) # tuple of args for foo
            # do some other stuff in the main process
            #boundingBox = async_result.get()  # get the return value from your function.
            
            boundingBox = self.getBoundingBox(image, targetName)
            if (boundingBox != None):
                accuracy, x, y, w, h = list(boundingBox)
                cv2.rectangle(image, (x, y), (w, h), (255, 0, 0), 2)
                cv2.putText(image, targetName + ' at %.2f' % (accuracy*100) , (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)
                self.display("Perception", image)
                return [x - 32, y - 24]

    def getBoundingBox(self, image, targetName):
        # bounding Box (accuracy, x, y, w, h)
        bounding_boxes = (0.0, 0.0, 0.0, 0.0, 0.0)
        ROI_SIZE = (130,130)
        INPUT_SIZE = (64, 48)

        # loop over the image pyramid
        for image in image_pyramid(image):
            for (x, y, roiOrig) in sliding_window(image, 32, ROI_SIZE):
                img = np.zeros([1, 48, 64, 3])
                img[0,:] = cv2.resize(roiOrig, (64, 48))
                prediction = self.model(img, training=False)[0]
                objectPrediction = prediction[self.classes.index(targetName)]
                if (objectPrediction > 0.95):
                    if (objectPrediction > bounding_boxes[0]):
                        bounding_boxes = (objectPrediction, x, y, x + ROI_SIZE[0], y + ROI_SIZE[1])
                    else:
                        return bounding_boxes


    def analyseEnvironment (self):  

        # Determine the object detected
        self.classifications.append(self.classes[np.argmax(prediction)])
        cv2.waitKey(1)

        """# Generate a single distorted bounding box.
        begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(tf.shape(top_image), bounding_boxes="", min_object_covered=0.1)
        print(begin, size)"""