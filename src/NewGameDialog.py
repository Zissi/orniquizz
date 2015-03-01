'''
Created on 02.02.2014

@author: zissi
'''
from PyQt4.QtGui import QDialog
from PyQt4 import uic
from PyQt4.QtCore import pyqtSignature

class NewGameDialog(QDialog):
    """Dialog for starting a new game."""

    def __init__(self, points, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi("ui/NewGameDialog.ui", self)
        self.ResultLabel.setText("Total points : " + str(points))

    @pyqtSignature("")
    def on_NewGameButton_clicked(self):
        self.accept()