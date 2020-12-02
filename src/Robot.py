import math
import time
import random
from threading import Thread
from queue import Queue
from qibullet import PepperVirtual
from src.Perception import Perception
from src.Communication import Communication
from concurrent.futures import ThreadPoolExecutor

class Robot(Thread):

    min_laser_value = 1.5 # Constante 

    def __init__(self, sim, client):
        Thread.__init__(self)
        self.pepper = sim.spawnPepper(client, spawn_ground_plane=True)
        self.perception = Perception(self.pepper)
        self.com = Communication(self)
        self.tasks = Queue()
        self.taskCanceled = False

    def run(self):
        self.perception.start()
        self.com.start()
        self.posture('stand')
        while True:
            if (not self.tasks.empty()):
                self.doTask(self.tasks.get())
            
            if self.taskCanceled:
                self.stop()
                self.taskCanceled = False

    def doTask(self, task):
        orderType, orderContent = task

        if (orderType == "find"):
            self.posture('search')
            result = self.find(orderContent)
            if (result):
                self.posture('point')
                self.com.say("Found !")
            else:
                self.posture('notFound')
                self.com.say("Sorry, I found nothing !")
            
        elif (orderType == "moveTo"):
            x, y = orderContent
            self.moveTo(x,y,math.atan2(y,x))
            self.com.say("I have reached my destination !")

        elif (orderType == "lookAt"):
            self.posture('search')
            x, y = orderContent
            self.moveTo(0,0,math.atan2(y,x))

            self.com.say("Nice view !")

        elif (orderType == "follow"):
            self.posture('search')
            if self.find(orderContent):
                self.follow(orderContent)
            else:
                self.posture('notFound')
                self.com.say("Sorry, I found nothing !")
        
        self.posture('stand')

    def stop(self):
        self.pepper.stopMove()

    def follow(self, target):
        pool = ThreadPoolExecutor(max_workers=1)
        while(not self.taskCanceled):
            result = self.perception.findLocationInScreen(target)
            if result != None:
                #x, y = result
                x, y = self.getPosition()
                self.moveTo(x + math.cos(self.getRotation()), y + math.sin(self.getRotation()), 0)
                #self.move(1,1,0)
                #self.moveTo(np.linalg.norm([x + math.cos(self.getRotation()),y + math.sin(self.getRotation()),0]), 0, 0)
                
                
                
            else:
                self.stop()



        

    def find(self, target):
        result = False
        while(not self.taskCanceled):
            # 8 * PI/4 = 2PI
            for i in range(10):
                self.moveTo(0.0, 0.0, math.pi/5)
                result = self.perception.find(target)
                if result or self.taskCanceled:
                    break
            break
        return result

    # Turn the robot left (+1) or right (-1)
    def switch_lane (self, direction):
        self.pepper.moveTo(0, 0, 0, frame=FRAME_ROBOT, speed=1, _async=True)
        time.sleep(1)
        self.pepper.moveTo(0, 0, direction * math.pi/2, frame=FRAME_ROBOT, speed=1, _async=False)
        self.pepper.moveTo(1, 0, 0, frame=FRAME_ROBOT, speed=1, _async=False)
        self.pepper.moveTo(0, 0, direction * -math.pi/2, frame=FRAME_ROBOT, speed=1, _async=False)
        self.pepper.moveTo(DESTINATION, 0, 0, frame=FRAME_ROBOT, speed=0.3, _async=True)

    def getPosition(self):
        x, y, theta = self.pepper.getPosition()
        return [x, y]

    def getRotation(self):
        x, y, theta = self.pepper.getPosition()
        return theta

    # stop robot
    def stop(self):
        self.pepper.stopMove()

    # speed
    def move(self, x, y, theta):
        self.pepper.move(x,y,theta)

    # move to crd
    def moveTo(self,x,y,theta,asyncMode=False): 
        self.pepper.moveTo(x,y,theta,_async=asyncMode,speed=0.6)

    def wander(self): # Deplacement sans but precis
        randomX = random.randint(-2,2)
        randomY = random.randint(-2,2)
        self.moveTo(randomX, randomY)

    def posture(self, name):
        if name == "stand":
            self.pepper.goToPosture("Stand", 1)
        elif name == "point":
            self.pepper.setAngles("LShoulderPitch", 0.09, 1)
            self.pepper.setAngles("LShoulderRoll", -0.4, 1)
            self.pepper.setAngles("LElbowYaw", 0.05, 1)
            self.pepper.setAngles("LElbowRoll", 0.4, 1)
            self.pepper.setAngles("LWristYaw", 0.7, 1)
            self.pepper.setAngles("LHand", 1, 1)
            time.sleep(3)
            self.posture('stand')
        elif name == "notFound":
            self.pepper.setAngles('HeadYaw', -0.3,1)
            time.sleep(1)
            self.pepper.setAngles('HeadYaw', 0.3,1)
            time.sleep(1)
            self.pepper.setAngles('HeadYaw', 0,1)
        elif name == "crouch":
            self.pepper.goToPosture("Crouch", 1)
        elif name == "search":
            self.pepper.setAngles("HeadPitch", 0.3, 1)
        time.sleep(1)


    
        


    