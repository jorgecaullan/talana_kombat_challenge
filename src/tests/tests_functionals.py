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
        """Set up the TestClient"""
        cls.client = TestClient(app)

    def load_json(self, file_name):
        """Easy load a json from tests data"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'data', file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def test_example1(self):
        """Test example1 from challenge instructions"""
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
            "Arnaldor gana la pelea y aun le queda 2 de energía"
        )

        self.assertEqual(response_json['details'], expected_details)
        self.assertEqual(response_json['winner'], "Arnaldor")
        self.assertEqual(len(response_json['warnings']), 0)

    def test_example2(self):
        """Test example2 from challenge instructions"""
        data = self.load_json('example2.json')
        response = self.client.post('/start', json=data)
        response_json = response.json()

        expected_details = (
            "Tonyn se mueve y da una patada\n"
            "Arnaldor se mueve y da un puñetazo\n"
            "Tonyn conecta un Taladoken\n"
            "Arnaldor se mueve y da una patada\n"
            "Tonyn se mueve y da una patada\n"
            "Arnaldor se mueve y da una patada\n"
            "Tonyn conecta un Taladoken\n"
            "Tonyn gana la pelea y aun le queda 3 de energía"
        )

        self.assertEqual(response_json['details'], expected_details)
        self.assertEqual(response_json['winner'], "Tonyn")
        self.assertEqual(len(response_json['warnings']), 0)

    def test_example3(self):
        """Test example3 from challenge instructions"""
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
            "Arnaldor gana la pelea y aun le queda 3 de energía"
        )

        self.assertEqual(response_json['details'], expected_details)
        self.assertEqual(response_json['winner'], "Tonyn")
        self.assertIn("Tonyn se queda sin movimientos", response_json['warnings'])

        # "Se acabó la pelea, Arnaldor gana, a quien le queda 3 de energía vs 1 de energía a Tonyn"


if __name__ == '__main__':
    unittest.main()
