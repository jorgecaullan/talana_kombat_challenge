""" Main file that run unit tests validating multiple combination moves of any player """
import unittest
import json
import os
from fastapi.testclient import TestClient
from main import app

class TestMultipleFights(unittest.TestCase):
    """Class that run all test data"""

    @classmethod
    def setUpClass(cls):
        """ Set up the TestClient """
        cls.client = TestClient(app)

    def load_json(self, file_name):
        """Easy load a json from tests data"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'data', file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def test_example1(self):
        """ Test example1 from challenge instructions """
        data = self.load_json('example1.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Tonyn avanza y da una patada\n"
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor se mueve\n"
            "Tonyn se agacha\n"
            "Arnaldor conecta un Remuyuken\n"
            "KO! Arnaldor gana la pelea y aun le queda 2 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")

    def test_example2(self):
        """ Test example2 from challenge instructions """
        data = self.load_json('example2.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Tonyn se mueve y da una patada\n"
            "Arnaldor se mueve y da un puñetazo\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor se mueve y da una patada\n"
            "Tonyn se mueve y da una patada\n"
            "Arnaldor avanza y conecta un Remuyuken\n"
            "Tonyn conecta un Taladoken\n"
            "KO! Tonyn gana la pelea y aun le queda 1 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Tonyn")

    def test_example3(self):
        """ Test example3 from challenge instructions """
        data = self.load_json('example3.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Arnaldor da un puñetazo\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor se mueve\n"
            "Tonyn se agacha\n"
            "Arnaldor se mueve y da un puñetazo\n"
            "Tonyn se queda inmóvil\n"
            "Arnaldor avanza y da una patada\n"
            "Tonyn se queda inmóvil\n"
            "Arnaldor da una patada\n"
            "Tonyn se queda inmóvil\n"
            "Arnaldor conecta un Remuyuken\n"
            "KO! Arnaldor gana la pelea y aun le queda 3 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")

    def test_less_hits_than_movements(self):
        """ Test less_hits_than_movements """
        data = self.load_json('less_hits_than_movements.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Tonyn avanza y da un puñetazo\n"
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn retrocede\n"
            "Arnaldor conecta un Remuyuken\n"
            "KO! Arnaldor gana la pelea y aun le queda 5 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")

    def test_less_movements_than_hits(self):
        """ Test less_movements_than_hits """
        data = self.load_json('less_movements_than_hits.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Arnaldor se mueve\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor avanza y conecta un Remuyuken\n"
            "Tonyn conecta un Remuyuken\n"
            "Arnaldor da un puñetazo\n"
            "Tonyn da un puñetazo\n"
            "KO! Tonyn gana la pelea y aun le queda 2 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Tonyn")

    def test_not_finished_fight_draw(self):
        """ Test not_finished_fight_draw """
        data = self.load_json('not_finished_fight_draw.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor da un puñetazo\n"
            "Tonyn conecta un Remuyuken\n"
            "Arnaldor da un puñetazo\n"
            "Tonyn salta hacia atrás\n"
            "Se acabó el tiempo! la pelea terminó en un Empate, "
            "a ambos jugadores les queda 1 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Draw")

    def test_not_finished_fight(self):
        """ Test not_finished_fight """
        data = self.load_json('not_finished_fight.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor da un puñetazo\n"
            "Tonyn conecta un Remuyuken\n"
            "Arnaldor se queda inmóvil\n"
            "Tonyn salta hacia atrás\n"
            "Se acabó el tiempo! Tonyn gana, "
            "a quien le queda 2 de energía vs a Arnaldor a quien le queda 1 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Tonyn")

    def test_not_strings_hits(self):
        """ Test not_strings_hits """
        data = self.load_json('not_strings_hits.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Tonyn se mueve\n"
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn se mueve\n"
            "Arnaldor se queda inmóvil\n"
            "Tonyn salta hacia atrás\n"
            "Arnaldor conecta un Remuyuken\n"
            "KO! Arnaldor gana la pelea y aun le queda 6 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")

    def test_not_strings_movements(self):
        """ Test not_strings_movements """
        data = self.load_json('not_strings_movements.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor se queda inmóvil\n"
            "Tonyn conecta un Remuyuken\n"
            "Arnaldor conecta un Remuyuken\n"
            "KO! Arnaldor gana la pelea y aun le queda 1 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")

    def test_with_just_player1(self):
        """ Test with_just_player1 """
        data = self.load_json('with_just_player1.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Arnaldor se queda inmóvil\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor se queda inmóvil\n"
            "Tonyn conecta un Taladoken\n"
            "KO! Tonyn gana la pelea y aun le queda 6 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Tonyn")

    def test_with_just_player2(self):
        """ Test with_just_player2 """
        data = self.load_json('with_just_player2.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Tonyn se queda inmóvil\n"
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn se queda inmóvil\n"
            "Arnaldor conecta un Remuyuken\n"
            "KO! Arnaldor gana la pelea y aun le queda 6 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")

    def test_without_players(self):
        """ Test without_players """
        data = self.load_json('without_players.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Se acabó el tiempo! la pelea terminó en un Empate, "
            "a ambos jugadores les queda 6 de energía"
        )

        self.assertEqual(response_json['detail'], expected_details)
        self.assertEqual(response_json['winner'], "Draw")

if __name__ == '__main__':
    unittest.main()
