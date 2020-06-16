import random

from game import *
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.dqn import AIAgent

if __name__ == '__main__':
    # Normal game, 4 players, 3 random and 1 human
    game = Game([RandomAgent(), RandomAgent(), AIAgent('./models/checkpoint1592262984.949143'), HumanAgent()], True)
    # print(game.deck)
    print(game.observation().shape)
    while not game.done():
        game.next_turn()
