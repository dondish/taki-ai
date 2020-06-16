import random

from game import *
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.dqn import AIAgent

if __name__ == '__main__':
    # Normal game, 4 players, 3 DQN agents and 1 human
    agents = [AIAgent('./models/checkpoint1592326865.162749'), AIAgent('./models/checkpoint1592326865.162749'),
                 AIAgent('./models/checkpoint1592326865.162749'), HumanAgent()]
    random.shuffle(agents)
    game = Game(agents, True)
    # print(game.deck)
    print(game.observation().shape)
    while not game.done():
        game.next_turn()
