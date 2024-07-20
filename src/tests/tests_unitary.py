""" Main file that run unit tests validating multiple combination moves of any player """
import unittest
from main import TalanaKombat

class TestMultipleFights(unittest.TestCase):
    """Class that run all test data"""

    def setUp(self):
        self.game = TalanaKombat()

    def test_player_1_movements_without_hits(self):
        """Test player 1 movements when doesn't use any hit"""

        self.assertEqual(self.game.get_movement_description('Tonyn', "", ""),
                         "Tonyn se queda inmóvil")
        self.assertEqual(self.game.get_movement_description('Tonyn', "D", ""),
                         "Tonyn avanza")
        self.assertEqual(self.game.get_movement_description('Tonyn', "A", ""),
                         "Tonyn retrocede")
        self.assertEqual(self.game.get_movement_description('Tonyn', "WS", ""),
                         "Tonyn salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Tonyn', "SW", ""),
                         "Tonyn salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Tonyn', "WA", ""),
                         "Tonyn salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Tonyn', "AW", ""),
                         "Tonyn salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Tonyn', "ASD", ""),
                         "Tonyn se mueve")
        self.assertEqual(self.game.get_movement_description('Tonyn', "DSA", ""),
                         "Tonyn se mueve")

if __name__ == '__main__':
    unittest.main()
