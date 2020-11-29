import sys
import Simulation
#from src.Simulation import Simulation


def runSimulation():
    sim = Simulation()


def trainPerception():
    print("perception")


def trainCommunication():
    print("communication")


if __name__ == "__main__":

    if (len(sys.argv) > 2):
        if (sys.argv[1] in ["-t", "--train"] and len(sys.argv) > 3):
            if (sys.argv[2] == "perception"):
                trainPerception()
            elif(sys.argv[2] == "communication"):
                trainCommunication()
            
        else:
            print("""Usage:
                -t --train <module>     to train module specified
            """)

    else:
        runSimulation()