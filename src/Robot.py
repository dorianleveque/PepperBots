import math
import time
from threading import Thread
from qibullet import PepperVirtual
from src.Perception import Perception



class Robot(Thread):
    def __init__(self, sim, client):
        Thread.__init__(self)
        #self.th = Thread(target=pepperBehavior)
        self.pepper = sim.spawnPepper(client, spawn_ground_plane=True)

        self.threads = [
            Perception(self.pepper)
        ]
        #self.th.start()
    

    def run(self):
        while True:
            print("hello")
        #self.threads[1].save_img()
    
    def moveTo(self,x,y): 
        self.pepper.moveTo(x,y,math.atan2(y,x))

    def idle(self): # Thread fonction
        self.pepper.goToPosture("Stand", 1)
        time.sleep(2.0)
        self.pepper.goToPosture("Crouch", 1)

    def pepperBehavior(self):
        self.idle()
    