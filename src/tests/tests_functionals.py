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

        # Call the POST /start endpoint
        response = self.client.post('/start', json=data)

        # Convert the response to JSON
        response_json = response.json()

        expected_details = (
            "Tonyn avanza y da una patada\n"
            "Arnaldor conecta un Remuyuken\n"
            "Tonyn usa un Taladoken\n"
            "Arnaldor se mueve\n"
            "Tonyn le da un puñetazo al pobre Arnaldor\n"
            "Arnaldor conecta un Remuyuken"
        )

        self.assertEqual(response_json['details'], expected_details)
        self.assertEqual(response_json['winner'], "You win")
        self.assertIn("No warnings", response_json['warnings'])

if __name__ == '__main__':
    unittest.main()
