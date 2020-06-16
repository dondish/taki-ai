import random

from game import *
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.dqn import AIAgent

if __name__ == '__main__':
    # Normal game, 4 players, 3 DQN agents and 1 human
    game = Game([AIAgent('./models/checkpoint1592310334.794725'), AIAgent('./models/checkpoint1592310334.794725'),
                 AIAgent('./models/checkpoint1592310334.794725'), HumanAgent()], True)
    # print(game.deck)
    print(game.observation().shape)
    while not game.done():
        game.next_turn()
