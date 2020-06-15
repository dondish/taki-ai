from torch import nn
from game import Agent, Action


class AIAgent(nn.Module):

    def __init__(self):
        super(AIAgent, self).__init__()

    def play(self, game):
        pass
