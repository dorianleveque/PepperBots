import time
from src.Robot import Robot
import cv2
from qibullet import PepperVirtual, SimulationManager
import pybullet


class Simulation:
    """
    Classe gérant la simu
    """

    def __init__(self):
        self.sim = SimulationManager()
        self.client = self.sim.launchSimulation()
        self.robot = Robot(self.sim, self.client)
        self.creerScene()

    def run(self):
        self.robot.start()
        """
        handle = pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)
        try:
            while True:
                img = pepper.getCameraFrame(handle)
                cv2.imshow("bottom camera", img)
                cv2.waitKey(1)

        except KeyboardInterrupt:
            self.simulation_manager.stopSimulation(client)
        """

    def creerScene(self):
        print("TODO")


    def getPepper(self):
        return self.pepper

    def getClient(self):
        return self.client

    def getSimulationManager(self):
        return self.simulationManager
