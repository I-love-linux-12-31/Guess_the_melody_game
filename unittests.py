import os.path
import unittest

from main import Game

class TestGame(unittest.TestCase):
    def test_update_score(self):
        game = Game()
        game.scores = [1, 1, 0]
        game.update_score([1, 2, -1])
        assert game.scores == [2, 3, -1]
        assert game.update_score([-1, -2, +1]) == game.scores
        assert game.scores == [1, 1, 0]

    def test_next_task(self):
        game = Game()
        answers = game.current_variants.copy()
        solution = game.current_solution
        game.next_task()
        assert game.current_variants != answers
        assert game.current_solution != solution

    def test_get_solution(self):
        game = Game()
        assert game.get_solution() == game.current_solution

    def test_get_answers(self):
        game = Game()
        assert game.current_variants == game.current_variants

    def test_get_music_file(self):
        game = Game()
        game.current_file = "resources/music/Lemon Knife - Red Stage.mp3"
        assert os.path.exists(game.get_music_file())
