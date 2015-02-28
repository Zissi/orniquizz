'''
Created on 11.03.2014

@author: zissi
'''
from PyQt4.QtGui import QMainWindow, QPixmap
from PyQt4.QtCore import pyqtSignature, Qt

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        pass
        

    def get_media(self, birds):
        imagepath = birds[self.answerfolder]["Image"]
        answerImage = QPixmap(imagepath).scaled(1000, 1000, Qt.KeepAspectRatio)
        self.bild1.setPixmap(answerImage) #sollte dieser letzte Teil dann im Main window passieren und dieses nur den Imagepath returnen?
