import os.path
import unittest

from main import Game
import main

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


class TestApp(unittest.TestCase):
    def test_correct_answer(self):
        app = main.QApplication([])
        window = main.MainWindow()
        _index = window.game.current_variants.index(window.game.get_solution())
        window.answers[_index].setChecked(True)
        window.submit()
        assert window.game.scores == [1, 0, 0]

    def test_incorrect_answer(self):
        app = main.QApplication([])
        window = main.MainWindow()
        _index = window.game.current_variants.index(window.game.get_solution())
        window.answers[(_index + 1) % 3].setChecked(True)
        window.submit()
        assert window.game.scores == [0, 0, 0]
        assert window.current_player == 1

    def test_end_game(self):
        app = main.QApplication([])
        window = main.MainWindow()
        _index = window.game.current_variants.index(window.game.get_solution())
        window.answers[_index].setChecked(True)
        window.submit()
        window.end_game()
        assert str(window.end_of_game.labels[0].text()).startswith("User1")
