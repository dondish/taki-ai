import random
random.seed(0)

from game import *
from agents.random import RandomAgent
from agents.human import HumanAgent

if __name__ == '__main__':
    # Normal game, 4 players, 3 random and 1 human
    game = Game([RandomAgent(0), RandomAgent(0), RandomAgent(0), HumanAgent()], True)
    # print(game.deck)
    print(game.observation().shape)
    while not game.done():
        game.next_turn()
