from src.NewGameDialog import NewGameDialog
from src.ChooseGame import ChooseGame
from src.Translator import Translator

from PyQt4.QtGui import QMainWindow, QPixmap
from PyQt4.QtCore import pyqtSignature, Qt
from PyQt4 import uic
from PyQt4.phonon import Phonon

import sys
from src.quiz.ImageQuiz import ImageQuiz
from src.quiz.AudioQuiz import AudioQuiz
from src.quiz.CombinedQuiz import CombinedQuiz


class OrniquizzMainWindow(QMainWindow):
    """Code for handling the MainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi("ui/OrniquizzMainWindow.ui", self)

        self.totalturns = 10
        self.progressTurns.setMaximum(self.totalturns)
        self.buttons = [self.answerLeftTop, self.answerRightTop,
                        self.answerLeftBottom, self.answerRightBottom]
        self.points = 0
        self.turns = 0
        self.m_media = None
        self.translator = Translator("externals/ornidroid/ornidroid/assets/ornidroid.jpg")
        self.dummipicture = QPixmap("birds.png").scaled(1000, 1000, Qt.KeepAspectRatio)

        self._connect()

        self.on_actionNeues_Spiel_triggered()

    def _connect(self):
        self.answerLeftTop.clicked.connect(self.check_answers)
        self.answerLeftBottom.clicked.connect(self.check_answers)
        self.answerRightTop.clicked.connect(self.check_answers)
        self.answerRightBottom.clicked.connect(self.check_answers)
        self.next.clicked.connect(self.start_new_question)

    def start_choose_game(self):
        dialog = ChooseGame()
        accepted = dialog.exec_()
        if accepted:
            difficulty = str(dialog.chosenbutton.text()).lower()
            game_mode = dialog.modebutton.text()
            if game_mode == "Image":
                self.quiz = ImageQuiz(difficulty)
                self.quiz.prepared_image.connect(self.display_image)
            elif game_mode == "Audio":
                self.quiz = AudioQuiz(difficulty)
                self.quiz.prepared_audio.connect(self.display_audio)
            else:
                self.quiz = CombinedQuiz(difficulty)
                self.quiz.prepared_image.connect(self.display_image)
                self.quiz.prepared_audio.connect(self.display_audio)

    @pyqtSignature("")
    def start_question(self):
        self.reset_for_new_question()
        options = self.quiz.start_question()
        self.make_buttons(options)

    def reset_for_new_question(self):
        self.turns += 1
        self.bild1.setToolTip("")
        for button in self.buttons:
            button.setStyleSheet("")
            button.setEnabled(True)

    def getAudio(self, answer):
        soundpath = self.birds[answer]["Audio"]
        output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.m_media = Phonon.MediaObject(self)
        Phonon.createPath(self.m_media, output)
        self.m_media.setCurrentSource(Phonon.MediaSource(soundpath))
        self.m_media.play()

    @pyqtSignature("QString")
    def display_image(self, imagepath):
        answerImage = QPixmap(imagepath).scaled(1000, 1000, Qt.KeepAspectRatio)
        self.bild1.setPixmap(answerImage)

    @pyqtSignature("QString")
    def display_audio(self, audiopath):
        output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.m_media = Phonon.MediaObject(self)
        Phonon.createPath(self.m_media, output)
        self.m_media.setCurrentSource(Phonon.MediaSource(audiopath))
        self.m_media.play()

    def make_buttons(self, options):
        for idx, button in enumerate(self.buttons):
            name = self.translator.translate(options[idx])
            button.setText(name)

    @pyqtSignature("")
    def on_actionNeues_Spiel_triggered(self):
        self.reset()
        self.start_choose_game()
        self.start_question()

    def reset(self):
        if self.m_media is not None:
            self.m_media.stop()
        self.turns = 0
        self.points = 0
        self.progressTurns.setValue(self.turns)
        self.bild1.setPixmap(self.dummipicture)
        self.pointdisplay.display(self.points)

    def check_answers(self):
        if self.quiz.played_sound():
            self.m_media.stop()
        given_answer = self.sender().text()
        correct = self.quiz.check_answer(given_answer)
        if correct:
            self.correct_answer()
        else:
            self.wrong_answer()

        for button in self.buttons:
            button.setEnabled(False)

        self.bild1.setToolTip(self.quiz.get_meta_info())

        self.pointdisplay.display(self.points)
        self.progressTurns.setValue(self.turns)

    def correct_answer(self):
        self.points += 1
        self.sender().setStyleSheet("background-color: rgb(154,205,50)")

    def wrong_answer(self):
        self.sender().setStyleSheet("background-color: rgb(255,69,0)")
        for button in self.buttons:
            if self.quiz.check_answer(button.text()):
                button.setStyleSheet("background-color: rgb(154,205,50)")

    def start_new_question(self):
        if self.quiz.played_sound():
            self.m_media.stop()
        self.progressTurns.setValue(self.turns)

        if self.turns == self.totalturns:
            self.start_new_game_dialog()
        else:
            self.start_question()

    def start_new_game_dialog(self):
        dialog = NewGameDialog(self.points, self)
        success = dialog.exec_()
        if success:
            self.on_actionNeues_Spiel_triggered()

    @pyqtSignature("")
    def on_actionSchlie_en_triggered(self):
        sys.exit()
