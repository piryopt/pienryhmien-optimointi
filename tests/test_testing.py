import unittest

class TestTestingCapabilities(unittest.TestCase):

    def test_importing_user(self):
        from src.entities.user import User
        User("Moti Motivaatio", 15634019, "moti@motivaatio.com", False)

if __name__ == "__main__":
    unittest.main()