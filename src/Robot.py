import math
import time
from threading import Thread
from Perception import Perception
from qibullet import PepperVirtual



class Robot:
    def __init__(self, refSurPepper):
        self.th = Thread(target=pepperBehavior)
        self.pepper = refSurPepper
        self.perception = Perception()
        self.th.start()
    
    def __del__(self):
        self.th._stop()
    
    def moveTo(self,x,y): 
        self.pepper.moveTo(x,y,math.atan2(y,x))

    def dance(self): # Thread fonction
        return

    def pepperBehavior(self):
        self.pepper.goToPosture("Stand", 1)
        time.sleep(2.0)
        self.pepper.goToPosture("Crouch", 1)
    