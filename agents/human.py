# Defines a playable agent
from game import *


class HumanAgent:
    def display_moves(self, moves):
        return ',\n'.join(map(lambda ac: f"{ac[0]}{(' ' + str(ac[1])) if ac[1] is not None else ''}", moves))

    def play(self, game):
        print(f"It's your turn, Player {game.curr+1}.")
        print("Shown Card:", str(game.shown_card()))
        print("Your Cards:", ", ".join(map(str, game.hands[game.curr])))
        print("Valid Moves:\n", self.display_moves(game.valid_moves()))
        while True:
            cards = game.hands[game.curr]
            choice = input("Choose your move: ")
            if choice.startswith("play "):
                action = Action.PLAY_CARD
                fcards = list(filter(lambda c: str(c) == choice[5:].strip(), cards))
                if len(fcards) > 0:
                    return action, fcards[0]
                else:
                    print("Invalid card selected. Please try again.")
            elif choice == "draw":
                action = Action.DRAW
                return action, None
            elif choice == "close taki":
                action = Action.CLOSE_TAKI
                return action, None
            else:
                print("Invalid move. Please try again.")
