import sys
#from src.Simulation import Simulation
from src.TrainPerception import TrainPerception


def launchSimulation():
    sim = None  # Simulation()


def trainPerception():
    t = TrainPerception()


def trainCommunication():
    print("communication")


if __name__ == "__main__":

    if (len(sys.argv) > 2):
        if (sys.argv[1] in ["-t", "--train"] and len(sys.argv) > 2):
            if (sys.argv[2] == "perception"):
                trainPerception()
            elif(sys.argv[2] == "communication"):
                trainCommunication()
            
        else:
            print("""Usage:
                -t --train <module>     to train module specified
            """)

    else:
        launchSimulation()