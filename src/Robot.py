import math
import time
import random
from threading import Thread
from qibullet import PepperVirtual
from src.Perception import Perception



class Robot(Thread):

    min_laser_value = 1.5 # Constante 

    def __init__(self, sim, client):
        Thread.__init__(self)
        #self.th = Thread(target=pepperBehavior)
        self.pepper = sim.spawnPepper(client, spawn_ground_plane=True)

        self.threads = [
            Perception(self.pepper)
        ]
        #self.th.start()
    

    def run(self):
        pepper.showLaser(True)
        pepper.subscribeLaser()

        while True:
            self.idle()
            detectLeft, detectFront, detectRight = self.checkLasers()
            self.wander()
            time.sleep(3)
        #self.threads[1].save_img()
    
    def moveTo(self,x,y): 
        self.pepper.moveTo(x,y,math.atan2(y,x),1)

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

    def wander(self):
        randomX = random.randint(-20,20)
        randomY = random.randint(-20,20)
        self.moveTo(randomX, randomY)
        


    