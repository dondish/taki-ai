from enum import Enum
import numpy as np
import random


class Color(Enum):
    NONE = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4

    def __str__(self):
        if self is Color.NONE:
            return ""
        elif self is Color.RED:
            return "red"
        elif self is Color.YELLOW:
            return "yellow"
        elif self is Color.GREEN:
            return "green"
        elif self is Color.BLUE:
            return "blue"


class Type(Enum):
    TAKI = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    STOP = 10
    CHDIR = 11
    TPLUS = 12
    CHCOL = 13

    def __str__(self):
        if self is Type.TAKI:
            return "taki"
        elif self is Type.STOP:
            return "stop"
        elif self is Type.CHDIR:
            return "change direction"
        elif self is Type.TPLUS:
            return "2+"
        elif self is Type.CHCOL:
            return "change color"
        else:
            return str(self)


class Card:
    def __init__(self, cardtype, color=Color.NONE):
        """

        :param color(Color): The color of the card
        :param cardtype(Type): The type of the card
        """
        self.color = color
        self.type = cardtype

    def __str__(self):
        if self.type is Type.TAKI and self.color is Color.NONE:
            return "super taki"
        return f"{self.color}{' ' if not self.color is Color.NONE else ''}{self.type}"

    def amount(self):
        if self.type == Type.CHCOL:
            return 4
        return 2


class Action(Enum):
    PLAY_CARD = 0
    DRAW = 1
    CLOSE_TAKI = 2


class State(Enum):
    NORMAL = 0
    DRAW_TWO = 1
    TAKI = 2
    SUPER_TAKI = 3
    FINISHED = 4


class Agent:
    def __init__(self):
        self.hand = []

    def play(self, game, state):
        return


class Game:
    def __init__(self, agents):
        """

        :param agents(List):
        """
        assert 1 < len(agents) < 11
        self.agents = agents
        self.curr = 0
        self.dir = 0
        self.state = State.NORMAL
        self.deck = []
        self.discard = []
        for t in Type:
            if t == Type.CHCOL:
                self.deck.extend([Card(Type.CHCOL)] * 4)
            else:
                for color in Color:
                    self.deck.extend([Card(t, color)] * 2)
            if t == Type.TAKI:
                self.deck.extend([Card(t)] * 2)
        random.shuffle(self.deck)
        self.discard.append(self.deck.pop())
        self.hands = []
        for i in range(len(agents)):
            a = []
            for j in range(8):
                a.append(self.deck.pop())
            self.hands.append(a)

    def shown_card(self):
        return self.discard[-1]

    def next_turn(self):
        if self.done():
            return True
        agent = self.agents[self.curr]
        action, card = agent.play(self, self.observation(agent))
        if action == Action.PLAY_CARD:
            self.discard.append(card)
            if card.type == Type.TAKI:
                if card.color == Color.NONE:
                    self.state = State.SUPER_TAKI
                else:
                    self.state = State.TAKI


    def done(self):
        return self.state == State.FINISHED

    def observation(self, agent):
        return np.array([self.state, 1, 2, 3, 4])
