import time
from src.Robot import Robot
import cv2
from qibullet import PepperVirtual, SimulationManager
import pybullet as pb
import pybullet_data as pd


class Simulation:
    """
    Classe gérant la simu
    """

    def __init__(self):
        self.sim = SimulationManager()
        self.client = self.sim.launchSimulation()
        self.robot = Robot(self.sim, self.client)
        self.createScene()
        self.robot.start()

    def run(self):
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

    def createScene(self):
        pb.setAdditionalSearchPath(pd.getDataPath())
        pb.loadURDF("duck_vhacd.urdf", basePosition=[4, 2, 0], globalScaling=5)
        pb.loadURDF("sphere2red.urdf", basePosition=[2, 0.05, 1], globalScaling=1)
        time.sleep(5)


    def getPepper(self):
        return self.pepper

    def getClient(self):
        return self.client

    def getSimulationManager(self):
        return self.simulationManager
