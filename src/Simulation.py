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
        self.simulationManager
        self.client
        self.pepper

    def run(self):
        self.simulation_manager = SimulationManager()
        self.client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
        robot = Robot(self.pepper)
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

    def getPepper(self):
        return self.pepper

    def getClient(self):
        return self.client

    def getSimulationManager(self):
        return self.simulationManager
