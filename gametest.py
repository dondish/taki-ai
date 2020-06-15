import unittest
from game import *


class ColorTest(unittest.TestCase):
    def test_repr(self):
        redtaki = Card(Type.TAKI, Color.RED)
        self.assertEqual(str(redtaki), "red taki")
        stop = Card(Type.STOP)
        self.assertEqual(str(stop), "stop")
        supertaki = Card(Type.TAKI)
        self.assertEqual(str(supertaki), "super taki")

    def test_action_to_scalar(self):
        playredtaki = Card(Type.TAKI, Color.RED)
        action = Action.PLAY_CARD
        self.assertEqual(action_to_scalar(action, playredtaki), 0)
        yellowthree = Card(Type.THREE, Color.YELLOW)
        self.assertEqual(action_to_scalar(action, yellowthree), 18)
        supertaki = Card(Type.TAKI)
        self.assertEqual(action_to_scalar(action, supertaki), 60)
        self.assertEqual(action_to_scalar(Action.DRAW, None), 61)
        self.assertEqual(action_to_scalar(Action.CLOSE_TAKI, None), 62)

    def test_scalar_to_action(self):
        playredtaki = Card(Type.TAKI, Color.RED)
        action = Action.PLAY_CARD
        self.assertEqual(scalar_to_action(0), (action, playredtaki))
        yellowthree = Card(Type.THREE, Color.YELLOW)
        self.assertEqual(scalar_to_action(18), (action, yellowthree))
        supertaki = Card(Type.TAKI)
        self.assertEqual((action, supertaki), scalar_to_action(60))
        self.assertEqual((Action.DRAW, None), scalar_to_action(61))
        self.assertEqual((Action.CLOSE_TAKI, None), scalar_to_action(62))

    def test_card_to_vector(self):
        playredtaki = Card(Type.TAKI, Color.RED)
        vec = card_to_vector(playredtaki)
        self.assertEqual(vec[0], 1)
        self.assertEqual(vec[1], 0)
        yellowthree = Card(Type.THREE, Color.YELLOW)
        vec = card_to_vector(yellowthree)
        self.assertEqual(vec[18], 1)
        self.assertEqual(vec[0], 0)
        supertaki = Card(Type.TAKI)
        vec = card_to_vector(supertaki)
        self.assertEqual(vec[61], 1)
        self.assertEqual(vec[0], 0)
        chcol = Card(Type.CHCOL)
        vec = card_to_vector(chcol)
        self.assertEqual(vec[60], 1)
        self.assertEqual(vec[0], 0)
        vec = card_to_vector(supertaki, chcol)
        self.assertEqual(vec[61], 1)
        self.assertEqual(vec[60], 1)
        self.assertEqual(vec[0], 0)


if __name__ == '__main__':
    unittest.main()
