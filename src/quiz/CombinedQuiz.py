from src.quiz.GenericQuiz import GenericQuiz

from PyQt4.QtCore import pyqtSignal, QString

class CombinedQuiz(GenericQuiz):
    """Quiz with images and audio."""

    prepared_image = pyqtSignal(str)
    prepared_audio = pyqtSignal(str)

    def __init__(self, difficulty):
        GenericQuiz.__init__(self, difficulty)

    def prepare_media(self):
        image_path = self.birds[self.answer]["Image"]
        self.prepared_image.emit(QString(image_path))
        audio_path = self.birds[self.answer]["Audio"]
        self.prepared_audio.emit(QString(audio_path))

    def is_valid_answer(self, answer):
        return (self.birds[answer]["Image"] is not None and
                self.birds[answer]["Audio"] is not None)

    def played_sound(self):
        return True