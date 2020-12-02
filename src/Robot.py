import math
import time
import random
from threading import Thread
from queue import Queue
from qibullet import PepperVirtual
from src.Perception import Perception
from concurrent.futures import ThreadPoolExecutor
import re

class Robot(Thread):

    min_laser_value = 1.5 # Constante 

    def __init__(self, sim, client):
        Thread.__init__(self)
        self.pepper = sim.spawnPepper(client, spawn_ground_plane=True)
        self.perception = Perception(self.pepper)
        self.tasks = Queue()
        self.taskCanceled = False
        self.tasks.put(("follow", "go to 20 20"))

    def run(self):
        self.perception.start()
        while True:
            if (not self.tasks.empty()):
                self.doTask(self.tasks.get())
            
            if self.taskCanceled:
                self.stop()

    
    def doTask(self, task):
        orderType, orderContent = task

        if (orderType == "find"):
            self.find(orderContent)
            
        elif (orderType == "moveTo"):
            x, y = self.getPositionFromString(orderContent)
            self.moveTo(x,y,math.atan2(y,x))

        elif (orderType == "lookAt"):
            x, y = self.getPositionFromString(orderContent)
            self.moveTo(0,0,math.atan2(y,x))

        elif (orderType == "follow"):
            if self.find(orderContent):
                self.follow(orderContent)
            else:
                print("not found")


    def getPositionFromString(self, content):
        position = []
        matches = re.finditer(r"(\d+) (\d+)", content, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                position.append(int(match.group(groupNum)))
        return position

    def stop(self):
        self.pepper.stopMove()

    def follow(self, target):
        pool = ThreadPoolExecutor(max_workers=1)
        while(not self.taskCanceled):
            """result = self.perception.find(target)
            if result != None:
                # objectif devant
                #asyncResult = pool.apply_async(self.findLocationInScreen, (target)) # tuple of args for foo
                asyncCompute = pool.submit(self.perception.findLocationInScreen, (target))                
                while asyncCompute.running():
                    self.move(1, 1, 0)
                    print("dzeafazfa")
                objectPosition = asyncCompute.result()
                if objectPosition != None:
                    self.moveTo(0, 0, objectPosition[0]/32)
                    print("yolo")
                print("nonde")
                
            else:
                self.stop()

            # check obstacle"""
            print("new one")
            result = self.perception.findLocationInScreen(target)
            if result != None:
                #x, y = result
                x, y = self.getPosition()
                self.moveTo(x + math.cos(self.getRotation()), y + math.sin(self.getRotation()), 0)
                #self.move(1,1,0)
                #self.moveTo(np.linalg.norm([x + math.cos(self.getRotation()),y + math.sin(self.getRotation()),0]), 0, 0)
                
                print("yolo")
                
                
            else:
                self.stop()



        

    def find(self, target):
        result = False
        while(not self.taskCanceled):
            # 8 * PI/4 = 2PI
            for i in range(10):
                self.moveTo(0.0, 0.0, math.pi/5)
                result = self.perception.find(target)
                if result:
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

    def idle(self): # Pepper flex ! 
        self.pepper.goToPosture("Stand", 1)
        time.sleep(1.0)
        self.pepper.goToPosture("Crouch", 1)

    def checkLasers(self):
        laserRight = pepper.getRightLaserValue()
        laserFront = pepper.getFrontLaserValue()
        laserLeft = pepper.getLeftLaserValue()
        detectRight = lambda x : True if(laser <= min_laser_value for laser in laserRight) else False
        detectFront = lambda x : True if(laser <= min_laser_value for laser in laserFront) else False
        detectLeft = lambda x : True if(laser <= min_laser_value for laser in laserLeft) else False
        return detectLeft, detectFront, detectRight

    def wander(self): # Deplacement sans but precis
        randomX = random.randint(-20,20)
        randomY = random.randint(-20,20)
        self.moveTo(randomX, randomY)
        


    