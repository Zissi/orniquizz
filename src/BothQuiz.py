'''
Created on 11.03.2014

@author: zissi
'''
import random, os

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def get_media(self):
        
        imagepath = self.birds[answerfolder]["Image"]
        answerImage = QPixmap(imagepath).scaled(1000, 1000, Qt.KeepAspectRatio)
        self.bild1.setPixmap(answerImage)
    
        soundpath = self.birds[answerfolder]["Audio"]
        output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.m_media = Phonon.MediaObject(self)
        Phonon.createPath(self.m_media, output)
        self.m_media.setCurrentSource(Phonon.MediaSource(soundpath))
        self.m_media.play()
        
        #was mach ich hier? sollte ich von audio und image erben? aber da heißen die funktionen gleich
    def get_answerfolder(self):
        data = False
        while data == False:
            self.currentfolder = random.sample(self.birds, 1)[0]
            if self.birds[self.currentfolder][str("Audio")] is not None and self.birds[self.currentfolder][str("Image")] is not None:
                data = True 
        return self.currentfolder