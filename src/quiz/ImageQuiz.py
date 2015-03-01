from src.quiz.GenericQuiz import GenericQuiz

from PyQt4.QtCore import pyqtSignal, QString

class ImageQuiz(GenericQuiz):
    """Quiz with only images."""

    prepared_image = pyqtSignal(str)

    def __init__(self, difficulty):
        GenericQuiz.__init__(self, difficulty)

    def prepare_media(self):
        image_path = self.birds[self.answer]["Image"]
        self.prepared_image.emit(QString(image_path))

    def is_valid_answer(self, answer):
        return self.birds[answer]["Image"] is not None

    def played_sound(self):
        return False
