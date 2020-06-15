import random


class RandomAgent:
    def __init__(self, seed=random.seed):
        self.random = random.Random(seed)

    def play(self, game):
        return self.random.choice(game.valid_moves())
