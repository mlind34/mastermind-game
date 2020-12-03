import unittest
from terminal_game import *

# Test Suite for Mastermind Game


class FeedbackTests(unittest.TestCase):
    """Tests correct feedback based on player guesses"""
    @classmethod
    def setUpClass(cls) -> None:
        # single player game with no duplicates
        cls.test_game = Game(1, False)
        cls.test_game.solution = ['Y', 'R', 'G', 'B']

        # single player game with duplicates
        cls.test_game2 = Game(1, True)
        cls.test_game2.solution = ['R', 'G', 'R', 'Y']

    def test_1(self):
        guess = self.test_game.guess_row('B', 'G', 'R', 'Y')
        result = self.test_game.feedback(guess)
        expected = ['W', 'W', 'W', 'W']
        self.assertEqual(set(result), set(expected))

    def test_2(self):
        guess = self.test_game.guess_row('Y', 'Y', 'Y', 'Y')
        result = self.test_game.feedback(guess)
        expected = ['B']
        self.assertEqual(set(result), set(expected))

    def test_3(self):
        guess = self.test_game.guess_row('O', 'O', 'O', 'O')
        result = self.test_game.feedback(guess)
        expected = []
        self.assertEqual(set(result), set(expected))

    def test_4(self):
        guess = self.test_game.guess_row('Y', 'R', 'G', 'B')
        result = self.test_game.feedback(guess)
        expected = ['B', 'B', 'B', 'B']
        self.assertEqual(set(result), set(expected))

    def test_5(self):
        guess = self.test_game.guess_row('R', 'Y', 'Y', 'Y')
        result = self.test_game.feedback(guess)
        expected = ['W', 'W']
        self.assertEqual(set(result), set(expected))

    def test_6(self):
        guess = self.test_game2.guess_row('R', 'R', 'R', 'R')
        result = self.test_game2.feedback(guess)
        expected = ['B', 'B']
        self.assertEqual(set(result), set(expected))

    def test_7(self):
        guess = self.test_game2.guess_row('O', 'R', 'R', 'O')
        result = self.test_game2.feedback(guess)
        expected = ['B']
        self.assertEqual(set(result), set(expected))


if __name__ == '__main__':
    unittest.main()
