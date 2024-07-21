""" Main file that run unit tests validating multiple combination moves of any player """
import unittest
from talana_kombat import TalanaKombat

class TestMovementInputs(unittest.TestCase):
    """ Class that tests players movements """

    def setUp(self):
        self.game = TalanaKombat({})

    def test_player_1_movements(self):
        """ Test player 1 movements previous to use a hit """

        self.assertEqual(self.game.get_movement_description('Tonyn', ""),
                         "se queda inmóvil")
        self.assertEqual(self.game.get_movement_description('Tonyn', "W"),
                         "salta")
        self.assertEqual(self.game.get_movement_description('Tonyn', "A"),
                         "retrocede")
        self.assertEqual(self.game.get_movement_description('Tonyn', "S"),
                         "se agacha")
        self.assertEqual(self.game.get_movement_description('Tonyn', "D"),
                         "avanza")

        # jumps
        self.assertEqual(self.game.get_movement_description('Tonyn', "WD"),
                         "salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Tonyn', "DW"),
                         "salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Tonyn', "WA"),
                         "salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Tonyn', "AW"),
                         "salta hacia atrás")

        # any other combination should return "Tonyn se mueve"
        self.assertEqual(self.game.get_movement_description('Tonyn', "ASD"),
                         "se mueve")
        self.assertEqual(self.game.get_movement_description('Tonyn', "DSA"),
                         "se mueve")
        self.assertEqual(self.game.get_movement_description('Tonyn', "WASD"),
                         "se mueve")

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
                         "se queda inmóvil")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "W"),
                         "salta")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "A"),
                         "avanza")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "S"),
                         "se agacha")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "D"),
                         "retrocede")

        # jumps
        self.assertEqual(self.game.get_movement_description('Arnaldor', "WD"),
                         "salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "DW"),
                         "salta hacia atrás")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "WA"),
                         "salta hacia adelante")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "AW"),
                         "salta hacia adelante")

        # any other combination should return "Arnaldor se mueve"
        self.assertEqual(self.game.get_movement_description('Arnaldor', "ASD"),
                         "se mueve")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "DSA"),
                         "se mueve")
        self.assertEqual(self.game.get_movement_description('Arnaldor', "WASD"),
                         "se mueve")

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

    def test_turn_description(self):
        """ Test different turns full descriptions """
        # only movements
        self.assertEqual(self.game.get_turn_description("player1", "AAA", ""),
                         "Tonyn retrocede\n")
        self.assertEqual(self.game.get_turn_description("player1", "ASDAS", ""),
                         "Tonyn se mueve\n")

        # only hits
        self.assertEqual(self.game.get_turn_description("player1", "", "K"),
                         "Tonyn da una patada\n")
        self.assertEqual(self.game.get_turn_description("player1", "DSD", "P"),
                         "Tonyn conecta un Taladoken\n")

        # movements with hits
        self.assertEqual(self.game.get_turn_description("player1", "DD", "P"),
                         "Tonyn avanza y da un puñetazo\n")
        self.assertEqual(self.game.get_turn_description("player1", "WDDSD", "P"),
                         "Tonyn salta hacia adelante y conecta un Taladoken\n")

        # no movements and no hits
        self.assertEqual(self.game.get_turn_description("player1", "", ""),
                         "Tonyn se queda inmóvil\n")

    def test_set_first_player(self):
        """ Test who player should start """
        base_json = {
            "player1": { "movimientos": ["ASD"], "golpes": ["P"] },
            "player2": { "movimientos": ["ASD"], "golpes": ["P"] }
        }

        # p1 same buttons and hits
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player1")

        # p1 less buttons
        base_json["player1"]["movimientos"] = ["AS"]
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player1")
        base_json["player1"]["movimientos"] = ["ASD"]
        base_json["player1"]["golpes"] = [""]
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player1")

        # p1 same buttons, but less hits
        base_json["player1"]["movimientos"] = ["AS"]
        base_json["player1"]["golpes"] = [""]
        base_json["player2"]["movimientos"] = ["A"]
        base_json["player2"]["golpes"] = ["K"]
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player1")

        # p2 less buttons
        base_json["player1"]["movimientos"] = ["ASD"]
        base_json["player1"]["golpes"] = ["P"]
        base_json["player2"]["movimientos"] = ["AS"]
        base_json["player2"]["golpes"] = ["P"]
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player2")
        base_json["player2"]["movimientos"] = ["ASD"]
        base_json["player2"]["golpes"] = [""]
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player2")

        # p2 same buttons, but less hits
        base_json["player1"]["movimientos"] = ["A"]
        base_json["player1"]["golpes"] = ["P"]
        base_json["player2"]["movimientos"] = ["AS"]
        self.assertEqual(TalanaKombat(base_json).set_first_player(),
                         "player2")


if __name__ == '__main__':
    unittest.main()
