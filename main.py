from game import *
from agents.random import RandomAgent
from agents.human import HumanAgent

if __name__ == '__main__':
    # Normal game, 4 players, 3 random and 1 human
    game = Game([RandomAgent(), RandomAgent(), RandomAgent(), HumanAgent()], True)
    while not game.done():
        game.next_turn()