import random
from enum import Enum

import torch


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
    PLUSTWO = 12
    CHCOL = 13
    PLUS = 14

    def __str__(self):
        if self is Type.TAKI:
            return "taki"
        elif self is Type.STOP:
            return "stop"
        elif self is Type.CHDIR:
            return "change direction"
        elif self is Type.PLUSTWO:
            return "2+"
        elif self is Type.CHCOL:
            return "change color"
        elif self is Type.PLUS:
            return "+"
        else:
            return str(self.value)


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

    def __str__(self):
        if self is Action.PLAY_CARD:
            return "play"
        elif self is Action.DRAW:
            return "draw"
        else:
            return "close taki"


class State(Enum):
    NORMAL = 0
    DRAW_TWO = 1
    TAKI = 2
    SUPER_TAKI = 3
    FINISHED = 4
    PLUS = 5
    STOP = 6  # Internal State


def action_to_scalar(action, card):
    if action is Action.PLAY_CARD:
        if card.color is not Color.NONE:
            return (card.color.value-1) * 15 + card.type.value  # Play any non Super TAKI Card
        return 60  # Play SUPER TAKI
    elif action is Action.DRAW:
        return 61
    elif action is Action.CLOSE_TAKI:
        return 62


def scalar_to_action(scalar):
    if scalar < 60:
        cardtype = Type(scalar % 15)
        color = Color((scalar - cardtype) // 15 + 1)
        return Action.PLAY_CARD, Card(cardtype, color)
    elif scalar == 60:
        return Action.PLAY_CARD, Card(Type.TAKI)
    elif scalar == 61:
        return Action.DRAW, None
    else:
        return Action.CLOSE_TAKI, None


class Game:
    def __init__(self, agents, debug=False):
        """

        :param agents(List):
        """
        assert 1 < len(agents) < 11
        self.agents = agents
        self.curr = 0
        self.dir = 1
        self.state = State.NORMAL
        self.deck = []
        self.discard = []
        self.draw_num = 0
        for t in Type:
            if t == Type.CHCOL:
                self.deck.extend([Card(Type.CHCOL)] * 4)
            else:
                for color in Color:
                    if color is not Color.NONE:
                        self.deck.extend([Card(t, color)] * 2)
            if t == Type.TAKI:
                self.deck.extend([Card(t)] * 2)
        random.shuffle(self.deck)
        self.discard.append(self.deck.pop())
        self.hands = []
        self.debug = debug
        for i in range(len(agents)):
            a = []
            for j in range(8):
                a.append(self.deck.pop())
            self.hands.append(a)

    def shown_card(self):
        return self.discard[-1]

    def next_agent(self):
        self.curr = (self.curr + self.dir) % len(self.agents)

    def draw_card(self, agent, amount=1):
        for i in range(amount):
            if len(self.deck) == 0:
                self.deck.extend(self.discard[:-1])
                random.shuffle(self.deck)
                self.discard = self.discard[-1:]
            self.hands[agent].append(self.deck.pop())

    def process_action(self, action, card, agent):
        if action == Action.PLAY_CARD:
            if self.state is State.PLUS:
                self.state = State.NORMAL
            self.discard.append(card)
            self.hands[self.curr].remove(card)
            if card.type is Type.TAKI:
                if card.color is Color.NONE:
                    self.state = State.SUPER_TAKI
                else:
                    self.state = State.TAKI
            elif card.type is Type.PLUSTWO:
                if self.state is not State.TAKI and self.state is not State.SUPER_TAKI:
                    self.state = State.DRAW_TWO
                    self.draw_num += 1
            elif card.type is Type.CHCOL:
                pass  # it automatically changes the color of the card
            elif card.type is Type.STOP:
                if self.state is not State.TAKI and self.state is not State.SUPER_TAKI:
                    self.state = State.STOP
            elif card.type is Type.CHDIR:
                self.dir *= 1
            elif card.type is Type.PLUS:
                if self.state is not State.TAKI and self.state is not State.SUPER_TAKI:
                    self.state = State.PLUS
            if self.debug:
                print(f"Player {agent+1} played {str(card)}.")
        elif action is Action.CLOSE_TAKI:
            if self.shown_card().type is Type.STOP:
                self.state = State.STOP
            elif self.shown_card().type is Type.PLUS:
                self.state = State.PLUS
            elif self.shown_card().type is Type.PLUSTWO:
                self.state = State.DRAW_TWO
                self.draw_num += 1
            else:
                self.state = State.NORMAL
            if self.debug:
                print(f"Player {agent+1} closed the TAKI.")
        elif action is Action.DRAW:
            s = 0
            if self.state is State.DRAW_TWO:
                s += 2 * self.draw_num
                self.draw_num = 0
                self.state = State.NORMAL
            if s == 0:
                s = 1
            self.draw_card(agent, s)
            if self.debug:
                print(f"Player {agent+1} drew {s} cards.")

    def valid_moves(self, agent=None):
        if agent is None:
            agent = self.curr
        cards = self.hands[agent]
        res = []
        # Play Cards
        for card in cards:
            if self.state is State.DRAW_TWO:
                if card is State.DRAW_TWO:
                    res.append((Action.PLAY_CARD, card))
            elif self.state is State.SUPER_TAKI:
                res.append((Action.PLAY_CARD, card))
            elif self.shown_card().type is card.type \
                    or self.shown_card().color is card.color \
                    or self.shown_card().color is Color.NONE:
                if card.type is Type.CHCOL:
                    for i in Color:
                        if i is not Color.NONE:
                            res.append((Action.PLAY_CARD, Card(Type.CHCOL, i)))
                else:
                    res.append((Action.PLAY_CARD, card))
        # Draw Cards
        res.append((Action.DRAW, None))
        # Close TAKI
        if self.state is State.TAKI or self.state is State.SUPER_TAKI:
            res.append((Action.CLOSE_TAKI, None))
        return res

    def next_turn(self):
        if self.done():
            return True, self.curr
        agent = self.agents[self.curr]
        if self.debug:
            print(f"It's player {self.curr+1}'s turn.")
        action, card = agent.play(self)
        self.process_action(action, card, self.curr)
        if len(self.hands[self.curr]) == 0:
            self.state = State.FINISHED
            return True, self.curr
        if self.state == State.STOP:
            self.next_agent()
            self.state = State.NORMAL
        if self.state == State.NORMAL or self.state == State.DRAW_TWO:
            self.next_agent()
        return False, self.curr

    def done(self):
        return self.state == State.FINISHED

    def observation(self, agent):
        return torch.tensor(self.state)
