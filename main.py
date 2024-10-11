import sys
import os
import random

from pydub import AudioSegment

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QRadioButton,
    QPushButton,
)
from PyQt6.uic import loadUi

from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl


class EndOfTheGameWindow(QWidget):
    btn_exit: QPushButton

    def __init__(self, game):
        super().__init__()
        loadUi("end_of_the_game.ui", self)
        game: Game
        images = ["resources/usr_1.png", "resources/usr_2.png", "resources/usr_3.png"]

        data = list(sorted(zip(game.scores, images, game.player_names), key=lambda a: -a[0]))

        self.images: [QLabel, QLabel, QLabel] = [self.img_1, self.img_2, self.img_3]
        self.labels: [QLabel, QLabel, QLabel] = [self.label_1, self.label_2, self.label_3]

        emoji = ["🥇", "🥈", "🥉"]

        for i, (score, path, name) in enumerate(data):
            self.images[i].setPixmap(QPixmap(path))
            self.labels[i].setText(F"{name} - {emoji[i]}\nScore: {score}")

        self.btn_exit.clicked.connect(sys.exit)

        self.show()


class MainWindow(QWidget):
    answer_1: QRadioButton
    answer_2: QRadioButton
    answer_3: QRadioButton
    answer_4: QRadioButton

    btn_submit: QPushButton
    btn_next: QPushButton
    btn_play: QPushButton

    player_1_block: QWidget
    player_2_block: QWidget
    player_3_block: QWidget

    player_1_label: QLabel
    player_2_label: QLabel
    player_3_label: QLabel

    current_player: int

    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        self.game = Game()

        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

        self.players_blocks = [self.player_1_block, self.player_2_block, self.player_3_block]
        self.labels = [self.player_1_label, self.player_2_label, self.player_3_label]
        self.answers = [self.answer_1, self.answer_2, self.answer_3, self.answer_4]
        self.current_player = 0

        self.btn_play.clicked.connect(self.play_audio)
        self.btn_submit.clicked.connect(self.submit)
        self.btn_next.clicked.connect(self.end_game)

        self.next()
        self.update_user_selection_indicator()

        self.end_of_game = None

    def play_audio(self, file_path=None):
        if not isinstance(file_path, str):
            file_path = self.game.get_music_file()
        self.btn_play.setEnabled(False)
        self._player.setSource(QUrl.fromLocalFile(file_path))
        self._player.play()

    def stop_audio(self):
        self._player.stop()

    def end_game(self):
        self.end_of_game = EndOfTheGameWindow(self.game)
        self.hide()

    def next(self):
        self.game.next_task()
        answers = self.game.get_answers()
        for i, answer in enumerate(self.answers):
            answer.setText(answers[i])
            answer.setEnabled(True)
            answer.setStyleSheet("")
            self.btn_play.setEnabled(True)
            # self.btn_next.setEnabled(False)

    def submit(self):
        answer = [a for a in self.answers if a.isChecked()]

        print(f"Player {self.current_player}: submitted {answer}")

        self.stop_audio()
        if answer:
            if answer[0].text() == self.game.get_solution():
                print("Correct answer!")
                self.btn_submit.setStyleSheet("background-color: green;")
                self.repaint()
                self.btn_submit.setStyleSheet("")

                lst = [0, 0, 0]
                lst[self.current_player] = 1
                self.game.update_score(lst)
                self.next()
            else:
                print(F"Incorrect answer: {answer[0].text()}! Correct is: {self.game.get_solution()}")
                answer[0].setEnabled(False)
                answer[0].setStyleSheet("color: red;")

            self.current_player = (self.current_player + 1) % 3
            self.update_user_selection_indicator()

    def update_user_selection_indicator(self):
        for i, block in enumerate(self.players_blocks):
            block.setStyleSheet("")
            self.labels[i].setText(F"{self.game.player_names[i]}   Score: {self.game.scores[i]}")
            if i == self.current_player:
                block.setStyleSheet("background-color: #555555AA; border-radius: 6px;")


def create_random_fragment(input_path, output_path="resources/out.mp3", duration=45000) -> str:
    audio = AudioSegment.from_mp3(input_path)

    if len(audio) <= duration:
        print("Исходный файл короче 45 секунд. Копируем его целиком.")
        fragment = audio
    else:
        max_start_time = len(audio) - duration

        start_time = random.randint(0, max_start_time)

        fragment = audio[start_time:start_time + duration]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fragment.export(output_path, format="mp3")
    return output_path


class Game:
    player_names: [str, str, str]
    scores: [float, float, float]
    current_file: str
    current_solution: str
    current_variants: [str, ]

    def __init__(self, name1="User1", name2="User2", name3="User3"):
        self.player_names = [name1, name2, name3]
        self.scores = [0, 0, 0]

        self.current_file = "N/A"
        self.current_solution = "N/A"
        self.current_variants = ["1. ...", "2. ...", "3. ...", "4. ..."]

        self.next_task()

    def update_score(self, lst: [float, float, float]) -> [float, float, float]:
        self.scores[0] += lst[0]
        self.scores[1] += lst[1]
        self.scores[2] += lst[2]
        return self.scores

    def next_task(self):
        files = [i for i in os.listdir("resources/music")]
        if self.current_solution in files:
            files.remove(self.current_file)

        variants = set()

        for _ in range(4):
            c = random.choice(files)
            files.remove(c)
            variants.add(c)

        self.current_variants = list(map(lambda a: a[:-4], variants))
        print(self.current_variants)
        self.current_solution = random.choice(self.current_variants)

        self.current_file = create_random_fragment(F"resources/music/{self.current_solution}.mp3")

    def get_solution(self) -> str:
        return self.current_solution

    def get_answers(self) -> [str, ]:
        return self.current_variants

    def get_music_file(self) -> str:
        return self.current_file


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    main()
