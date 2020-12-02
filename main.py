import sys
import argparse
from src.Simulation import Simulation
from src.TrainPerception import TrainPerception
from src.chatbot_learning import make_chatbot_learning


def runSimulation():
    sim = Simulation()
    sim.start()

def trainPerception(regenerate):
    t = TrainPerception(regenerate)
    t.train()

def trainCommunication(regenerate):
    print("af")
    make_chatbot_learning()

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description="IML projet to test some ai feature and human / robot interaction.\nWe using qiBullet and machine learning.")
    #group = parser.add_mutually_exclusive_group()
    subparsers = parser.add_subparsers(help='commands')

    # A training command
    train_parser = subparsers.add_parser('train', help='Train model')
    train_parser.add_argument("model", action="store", choices=('communication', 'perception'), nargs='+')
    train_parser.add_argument("-g", "--regenerate", action="store_true", help="remove the previous dataset and regenerate a new one")
    
    args = parser.parse_args()
    print(args)

    if "model" in args:
        if ("perception" in args.model): 
            trainPerception(args.regenerate)
        elif("communication" in args.model):
            trainCommunication(args.regenerate)
    else:
        runSimulation()