from src.quiz.GenericQuiz import GenericQuiz

from PyQt4.QtCore import pyqtSignal, QString

class AudioQuiz(GenericQuiz):
    """Quiz with only audio."""

    prepared_audio = pyqtSignal(str)

    def __init__(self, difficulty):
        GenericQuiz.__init__(self, difficulty)

    def prepare_media(self):
        audio_path = self.birds[self.answer]["Audio"]
        self.prepared_audio.emit(QString(audio_path))

    def is_valid_answer(self, answer):
        return self.birds[answer]["Audio"] is not None

    def played_sound(self):
        return True
