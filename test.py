import unittest
from random_string_detector import RandomStringDetector

class Test(unittest.TestCase):
    def test_random_string(self):
        detector = RandomStringDetector()
        self.assertTrue(detector("aowkaoskaos"))

    def test_valid_string(self):
        detector = RandomStringDetector()
        self.assertFalse(detector("Hello World"))

    def test_valid_string_with_numbers(self):
        detector = RandomStringDetector()
        self.assertFalse(detector("Hello World 123"))

if __name__ == '__main__':
    unittest.main()