from src.BirdLoader import BirdLoader
from src.Translator import Translator

from PyQt4.QtCore import QObject

import random

class GenericQuiz(QObject):
    """Base class for all quiz types"""

    def __init__(self, difficulty="easy"):
        QObject.__init__(self)
        bird_loader = BirdLoader()
        self.translator = Translator()
        self.birds = bird_loader.load_birds()
        self.birds_played = []
        self.answer = None
        self.difficulty = difficulty

    def is_valid_answer(self, answer):
        raise NotImplementedError

    def prepare_media(self):
        raise NotImplementedError

    def played_sound(self):
        raise NotImplementedError

    def start_question(self):
        self.answer = self.get_answer()
        self.prepare_media()
        return self.get_options()

    def get_answer(self):
        data = False
        while not data:
            answer = random.sample(self.birds, 1)[0]
            if (answer not in self.birds_played and
                self.is_valid_answer(answer)):
                data = True
        return answer

    def check_answer(self, given_answer):
        displayed_answer = self.translator.translate(self.answer)
        return unicode(displayed_answer) == unicode(given_answer)

    def get_options(self):
        if self.difficulty == "easy":
            options = self.get_easy_options()
        elif self.difficulty == "intermediate":
            options = self.get_intermediate_options()
        else:
            options = self.get_difficult_options()
        all_options = options + [self.answer]
        random.shuffle(all_options)
        return all_options

    def get_difficult_options(self):
        samefamily = self.get_similar("Family")
        try:
            randomlist = random.sample(samefamily, 3)
        except ValueError:
            try:
                sameorder = self.get_similar("Order")
                randomlist = random.sample(samefamily, len(samefamily))
                randomlist = randomlist + random.sample(sameorder, 3 - len(samefamily))
            except ValueError:
                randomlist = random.sample(samefamily, len(samefamily))
                randomlist = randomlist + random.sample(sameorder, len(sameorder))
                randomlist = randomlist + random.sample(self.birds, 3 - len(samefamily) - len(sameorder))
        return randomlist

    def get_intermediate_options(self):
        sameorder = self.get_similar("Order")
        try:
            randomlist = random.sample(sameorder, 3)
        except ValueError:
            randomlist = random.sample(sameorder, len(sameorder))
            randomlist = randomlist + random.sample(self.birds, 3 - len(sameorder))
        return randomlist

    def get_easy_options(self):
        randomlist = random.sample(self.birds, 3)
        return randomlist

    def get_similar(self, similarity_level):
        family_order = self.birds[self.answer][similarity_level]
        same_family_order = []
        for bird in self.birds:
            if self.birds[bird][similarity_level] == family_order and bird != self.answer:
                same_family_order.append(bird)
        return same_family_order

    def get_meta_info(self):
        return self.birds[self.answer]["Scientific_Name"] + " " + self.birds[self.answer]["Habitat"]
