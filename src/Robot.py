import math
from Perception import Perception
from qibullet import PepperVirtual


class Robot:
    def __init__(self, refSurPepper):
        self.pepper = refSurPepper
        self.perception = Perception()
    
    def moveTo(self,x,y):
        self.pepper.moveTo(x,y,math.atan2(y,x))
    