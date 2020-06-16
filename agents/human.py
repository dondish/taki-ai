# Defines a playable agent
from game import *


class HumanAgent:
    def display_moves(self, moves):
        return ',\n'.join(map(lambda ac: f"{ac[0]}{(' ' + str(ac[1])) if ac[1] is not None else ''}", moves))

    def color_from_string(self, s):
        for i in Color:
            if str(i) == s:
                return i
        return Color.NONE

    def play(self, game):
        moves = game.valid_moves()
        print("--------------------------------------")
        print()
        print(f"It's your turn, Player {game.curr+1}.")
        print(f"Amounts of cards: {', '.join(map(str,map(len, game.hands)))}")
        print("Shown Card:", str(game.shown_card()))
        print("Your Cards:", ", ".join(map(str, game.hands[game.curr])))
        print("Valid Moves:\n", self.display_moves(moves))
        while True:
            cards = game.hands[game.curr]
            choice = input("Choose your move: ")
            if choice.startswith("play "):
                action = Action.PLAY_CARD
                if choice.strip().endswith("change color"):
                    fcards = list(filter(lambda c: c.type == Type.CHCOL, cards))
                    if len(fcards) > 0:
                        fcards[0] = Card(Type.CHCOL, self.color_from_string(choice[5:].split()[0].strip()))
                else:
                    fcards = list(filter(lambda c: str(c) == choice[5:].strip(), cards))
                if len(fcards) > 0 and (action, fcards[0]) in moves:
                    return action, fcards[0]
                else:
                    print("Invalid card selected. Please try again.")
            elif choice == "draw":
                action = Action.DRAW
                return action, None
            elif choice == "close taki" and (Action.CLOSE_TAKI, None) in moves:
                action = Action.CLOSE_TAKI
                return action, None
            else:
                print("Invalid move. Please try again.")
