import unittest

class TestTestingCapabilities(unittest.TestCase):

    def test_importing_algorithms(self):
        from algorithms.entities.user import User
        User(1, "FOO", [])

    def test_importing_src(self):
        from src.app import hello_world

if __name__ == "__main__":
    unittest.main()