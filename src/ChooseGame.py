'''
Created on 02.02.2014

@author: zissi
'''
from PyQt4.QtGui import QDialog
from PyQt4 import uic
from PyQt4.QtCore import pyqtSignature

class ChooseGame(QDialog):

    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        uic.loadUi("ui/ChooseGame.ui", self)
        self.EasyButton.clicked.connect(self.GameChosen)
        self.IntermediateButton.clicked.connect(self.GameChosen)
        self.HardButton.clicked.connect(self.GameChosen)
        self.ImageButton.clicked.connect(self.ModeChosen)
        self.AudioButton.clicked.connect(self.ModeChosen)
        self.BothButton.clicked.connect(self.ModeChosen)
        self.chosenbutton = self.IntermediateButton
        self.modebutton = self.ImageButton
        
    @pyqtSignature("")          
    def GameChosen(self):
        self.chosenbutton = self.sender()
    
    def ModeChosen(self):
        self.modebutton = self.sender()
    

        
    @pyqtSignature("")       
    def on_StartButton_clicked(self):
        self.accept()

        
        
        
