""" Main file that run tests """
import unittest
import json
import os

class TestMultipleFights(unittest.TestCase):
    """Class that run all test data"""

    def load_json(self, file_name):
        """Easy load a json from tests data"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'data', file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def test_example1(self):
        """Test example1 from challenge instructions"""
        example1 = self.load_json('example1.json')

        self.assertIn('player1', example1)
        self.assertIn('player2', example1)

if __name__ == '__main__':
    unittest.main()
