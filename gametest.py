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


if __name__ == '__main__':
    unittest.main()
