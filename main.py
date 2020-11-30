import sys
import argparse
from src.Simulation import Simulation
#from src.Simulation import Simulation
from src.TrainPerception import TrainPerception


def runSimulation():
    sim = Simulation()
    sim.start()


def trainPerception():
    t = TrainPerception()
    t.train()

def trainCommunication():
    print("communication")


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description="IML projet to test some ai feature and human / robot interaction.\nWe using qiBullet and machine learning.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--train", action="append", choices=('communication', 'perception'), help="train model")
    args = parser.parse_args()

    if args.train:
        if ("perception" in args.train): 
            trainPerception()
        elif("communication" in args.train):
            trainCommunication()
    else:
        runSimulation()