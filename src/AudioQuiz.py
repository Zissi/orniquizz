'''
Created on 02.03.2014

@author: zissi
'''

'''
Created on 02.03.2014

@author: zissi
'''
from src.Quiz import Quiz
from PyQt4.QtCore import pyqtSignature, Qt
from PyQt4.phonon import Phonon

class AudioQuiz(Quiz):
    
    def __init__(self, parent=None):
        self.m_media = None
    
    def get_media(self, birds):
        soundpath = birds[self.answerfolder]["Audio"]
        output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.m_media = Phonon.MediaObject(self)
        Phonon.createPath(self.m_media, output)
        self.m_media.setCurrentSource(Phonon.MediaSource(soundpath))
        self.m_media.play()


 