""" Main file that run unit tests validating multiple combination moves of any player """
import unittest
from main import TalanaKombat

class TestMovementInputs(unittest.TestCase):
    """ Class that tests players movements """

    def setUp(self):
        self.game = TalanaKombat()

    def test_player_1_movements(self):
        """ Test player 1 movements previous to use a hit """

        self.assertEqual(self.game.get_movement_description('Tonyn', ""),
                         "Tonyn se queda inmóvil")
        self.assertEqual(self.game.get_movement_description('Tonyn', "W"),
                         "Tonyn salta")
        self.assertEqual(self.game.get_movement_description('Tonyn', "A"),
                         "Tonyn retrocede")
        self.assertEqual(self.game.get_movement_description('Tonyn', "S"),
                         "Tonyn se agacha")
        self.assertEqual(self.game.get_movement_description('Tonyn', "D"),
                         "Tonyn avanza")

        # jumps
        self.assertEqual(self.game.get_movement_description('Tonyn', "WS"),
                         "Tonyn salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Tonyn', "SW"),
                         "Tonyn salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Tonyn', "WA"),
                         "Tonyn salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Tonyn', "AW"),
                         "Tonyn salta hacia atrás")

        # any other combination should return "Tonyn se mueve"
        self.assertEqual(self.game.get_movement_description('Tonyn', "ASD"),
                         "Tonyn se mueve")
        self.assertEqual(self.game.get_movement_description('Tonyn', "DSA"),
                         "Tonyn se mueve")
        self.assertEqual(self.game.get_movement_description('Tonyn', "WASD"),
                         "Tonyn se mueve")

    def test_player_1_hits(self):
        """ Test player 1 hits """

        self.assertEqual(self.game.get_hit_description('Tonyn', "", "P")["name"],
                         "da un puñetazo")
        self.assertEqual(self.game.get_hit_description('Tonyn', "", "K")["name"],
                         "da una patada")

        # Taladoken
        self.assertEqual(self.game.get_hit_description('Tonyn', "DSD", "P")["name"],
                         "conecta un Taladoken")
        composed_attack = self.game.get_hit_description('Tonyn', "WADSD", "P")
        self.assertEqual(composed_attack["name"], "conecta un Taladoken")
        self.assertEqual(composed_attack["damage"], 3)
        self.assertEqual(composed_attack["previous_movements"], "WA")

        # Remuyuken
        self.assertEqual(self.game.get_hit_description('Tonyn', "SD", "K")["name"],
                         "conecta un Remuyuken")
        composed_attack = self.game.get_hit_description('Tonyn', "WAASD", "K")
        self.assertEqual(composed_attack["name"], "conecta un Remuyuken")
        self.assertEqual(composed_attack["damage"], 2)
        self.assertEqual(composed_attack["previous_movements"], "WAA")

        # any other combination are just a punch or kick
        self.assertEqual(self.game.get_hit_description('Tonyn', "WADS", "P")["name"],
                         "da un puñetazo")
        self.assertEqual(self.game.get_hit_description('Tonyn', "WADS", "K")["name"],
                         "da una patada")

    def test_player_2_movements(self):
        """ Test player 2 movements previous to use a hit """

        self.assertEqual(self.game.get_movement_description('Arnaldor', ""),
                         "Arnaldor se queda inmóvil")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "W"),
                         "Arnaldor salta")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "A"),
                         "Arnaldor avanza")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "S"),
                         "Arnaldor se agacha")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "D"),
                         "Arnaldor retrocede")

        # jumps
        self.assertEqual(self.game.get_movement_description('Arnaldor', "WS"),
                         "Arnaldor salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "SW"),
                         "Arnaldor salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "WA"),
                         "Arnaldor salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "AW"),
                         "Arnaldor salta hacia adelante")

        # any other combination should return "Arnaldor se mueve"
        self.assertEqual(self.game.get_movement_description('Arnaldor', "ASD"),
                         "Arnaldor se mueve")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "DSA"),
                         "Arnaldor se mueve")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "WASD"),
                         "Arnaldor se mueve")

    def test_player_2_hits(self):
        """ Test player 2 hits """

        self.assertEqual(self.game.get_hit_description('Arnaldor', "", "P")["name"],
                         "da un puñetazo")
        self.assertEqual(self.game.get_hit_description('Arnaldor', "", "K")["name"],
                         "da una patada")

        # Taladoken
        self.assertEqual(self.game.get_hit_description('Arnaldor', "ASA", "P")["name"],
                         "conecta un Taladoken")
        composed_attack = self.game.get_hit_description('Arnaldor', "WAASA", "P")
        self.assertEqual(composed_attack["name"], "conecta un Taladoken")
        self.assertEqual(composed_attack["damage"], 2)
        self.assertEqual(composed_attack["previous_movements"], "WA")

        # Remuyuken
        self.assertEqual(self.game.get_hit_description('Arnaldor', "SA", "K")["name"],
                         "conecta un Remuyuken")
        composed_attack = self.game.get_hit_description('Arnaldor', "WAASA", "K")
        self.assertEqual(composed_attack["name"], "conecta un Remuyuken")
        self.assertEqual(composed_attack["damage"], 3)
        self.assertEqual(composed_attack["previous_movements"], "WAA")

        # any other combination are just a punch or kick
        self.assertEqual(self.game.get_hit_description('Arnaldor', "WADS", "P")["name"],
                         "da un puñetazo")
        self.assertEqual(self.game.get_hit_description('Arnaldor', "WADS", "K")["name"],
                         "da una patada")

if __name__ == '__main__':
    unittest.main()
