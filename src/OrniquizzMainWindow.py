from NewGameDialog import NewGameDialog
from ChooseGame import ChooseGame
from Translator import Translator

from PyQt4.QtGui import QMainWindow, QPixmap
from PyQt4.QtCore import pyqtSignature, Qt
from PyQt4 import uic
from PyQt4.phonon import Phonon

import random, os
import sys
try:
    import cPickle as pickle #Not available on some python distributions
except ImportError:
    import pickle


class OrniquizzMainWindow(QMainWindow):
    """Code for handling the MainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi("ui/OrniquizzMainWindow.ui", self)
        self.birds = self.loadOrCreateBirds()

        self.totalturns = 10
        self.progressTurns.setMaximum(self.totalturns)
        self.buttons = [self.answerLeftTop, self.answerRightTop,
                        self.answerLeftBottom, self.answerRightBottom]

        self.difficulty = ""
        self.game_mode = ""
        self.currentbird = None
        self.currentfolder = None
        self.points = 0
        self.turns = 0
        self.m_media = None
        self.wrong_answers = []
        self.answers = []
        self.birdsplayed = []

        self.answerLeftTop.clicked.connect(self.check_answers)
        self.answerLeftBottom.clicked.connect(self.check_answers)
        self.answerRightTop.clicked.connect(self.check_answers)
        self.answerRightBottom.clicked.connect(self.check_answers)

        self.next.clicked.connect(self.start_new_question)

        self.translator = Translator("externals/ornidroid/ornidroid/assets/ornidroid.jpg")

        self.dummipicture = QPixmap("birds.png").scaled(1000, 1000, Qt.KeepAspectRatio)

        self.on_actionNeues_Spiel_triggered()
    
    def loadOrCreateBirds(self):
        pickleName = "birds.pkl"
        if os.path.exists(pickleName):
            with open(pickleName) as pickleFile:
                birds = pickle.load(pickleFile)
        else:
            self.translator = Translator("externals/ornidroid/ornidroid/assets/ornidroid.jpg")
            birds = self.translator.createBirddic()
            with open(pickleName, "wb") as pickleFile:
                pickle.dump(birds, pickleFile, protocol=pickle.HIGHEST_PROTOCOL) 
        return birds
    
    def startChooseGame(self):
        dialog = ChooseGame()
        accepted = dialog.exec_()
        if accepted:
            self.difficulty = dialog.chosenbutton.text()
            self.game_mode = dialog.modebutton.text() #@TODO: else?

    @pyqtSignature("")
    def startQuestion(self):
        self.resetForNewQuestion()
        if self.game_mode == "Both":
            self.getAnswerBothquiz()
        else:
            self.getAnswerSinglequiz()

        self.getQuestionMedia()
        self.saveCurrentAnswer()

        if self.difficulty == "Hard":
            self.getDifficultAnswers()    
        elif self.difficulty == "Intermediate":
            self.getIntermediateAnswer()
        else:
            self.getEasyAnswer()

        self.combineAnswers()
        self.makeButtons()

    def getQuestionMedia(self):
        if self.game_mode == "Audio": 
            self.getAudio(self.currentfolder)  
        elif self.game_mode == "Image":
            self.getImage(self.currentfolder)
        elif self.game_mode == "Both":
            self.getAudio(self.currentfolder)
            self.getImage(self.currentfolder)

    def resetForNewQuestion(self):
        self.turns += 1
        self.bild1.setToolTip("") 
        for button in self.buttons:
            button.setStyleSheet("")
            button.setEnabled(True)

    def getAnswerSinglequiz(self):
        data = False
        while not data:
            self.currentfolder = random.sample(self.birds, 1)[0]
            if self.currentfolder not in self.birdsplayed and self.birds[self.currentfolder][str(self.game_mode)] is not None:
                data = True
        return self.currentfolder

    def getAnswerBothquiz(self):
        data = False
        while data == False:
            self.currentfolder = random.sample(self.birds, 1)[0]
            if self.birds[self.currentfolder][str("Audio")] is not None and self.birds[self.currentfolder][str("Image")] is not None:
                data = True 
        return self.currentfolder

    def saveCurrentAnswer(self):
        self.birdsplayed.append(self.currentfolder)
        self.currentbird = self.translator.translate(self.currentfolder)

    def getFamilyorOrder(self, difficulty):
        familyOrder = self.birds[self.currentfolder][difficulty]
        samefamilyOrder = []
        for bird in self.birds:
            if self.birds[bird][difficulty] == familyOrder and bird != self.currentfolder:
                samefamilyOrder.append(bird)
        return samefamilyOrder

    def getAudio(self, answer):
        soundpath = self.birds[answer]["Audio"]
        output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.m_media = Phonon.MediaObject(self)
        Phonon.createPath(self.m_media, output)
        self.m_media.setCurrentSource(Phonon.MediaSource(soundpath))
        self.m_media.play()

    def getImage(self, answer):
        imagepath = self.birds[answer]["Image"]
        answerImage = QPixmap(imagepath).scaled(1000, 1000, Qt.KeepAspectRatio)
        self.bild1.setPixmap(answerImage)

    def getDifficultAnswers(self):
        samefamily = self.getFamilyorOrder("Family")   
        try:
            randomlist = random.sample(samefamily, 3)
        except ValueError:
            try: 
                sameorder = self.getFamilyorOrder("Order")
                randomlist = random.sample(samefamily, len(samefamily))
                randomlist = randomlist + random.sample(sameorder, 3 - len(samefamily))
            except ValueError:
                randomlist = random.sample(samefamily, len(samefamily))
                randomlist = randomlist + random.sample(sameorder, len(sameorder))
                randomlist = randomlist + random.sample(self.birds, 3 - len(samefamily) - len(sameorder))
        self.wrong_answers = randomlist
        return randomlist

    def getIntermediateAnswer(self):
        sameorder = self.getFamilyorOrder("Order")
        try:
            randomlist = random.sample(sameorder, 3)
        except ValueError:
            randomlist = random.sample(sameorder, len(sameorder))
            randomlist = randomlist + random.sample(self.birds, 3 - len(sameorder))
        self.wrong_answers = randomlist
        return randomlist

    def getEasyAnswer(self):
        randomlist = random.sample(self.birds, 3)
        self.wrong_answers = randomlist
        return randomlist

    def combineAnswers(self):
        self.wrong_answers.append(self.currentfolder)
        random.shuffle(self.wrong_answers)

    def makeButtons(self):
        for idx, button in enumerate(self.buttons):
            gername = self.translator.translate(self.wrong_answers[idx])
            button.setText(gername)

    @pyqtSignature("")
    def on_actionNeues_Spiel_triggered(self):
        self.reset()
        self.startChooseGame()
        self.startQuestion()

    def reset(self):
        if self.m_media is not None: 
            self.m_media.stop() 
        self.turns = 0
        self.points = 0
        self.progressTurns.setValue(self.turns)  
        self.bild1.setPixmap(self.dummipicture) 
        self.pointdisplay.display(self.points) 

    def check_answers(self):
        if self.game_mode != "Image": #@TODO: refactor!
            self.m_media.stop()
        if self.sender().text() == self.currentbird:
            self.correctAnswer()
        else:
            self.wrongAnswer()

        for button in self.buttons:
            button.setEnabled(False)

        if self.answerLeftTop.isEnabled() == False:    
            self.bild1.setToolTip(self.birds[self.currentfolder]["Scientific_Name"] + " " + self.birds[self.currentfolder]["Habitat"])

        self.pointdisplay.display(self.points)
        self.progressTurns.setValue(self.turns) 

    def correctAnswer(self):
        self.points += 1
        self.sender().setStyleSheet("background-color: rgb(154,205,50)")

    def wrongAnswer(self):
        self.sender().setStyleSheet("background-color: rgb(255,69,0)")
        for button in self.buttons:
            if button.text() == self.currentbird:
                button.setStyleSheet("background-color: rgb(154,205,50)")

    def start_new_question(self):
        if self.game_mode != "Image":
            self.m_media.stop()
        self.progressTurns.setValue(self.turns) 

        if self.turns == self.totalturns:
            self.startNewGameDialog()
        else:
            self.startQuestion()

    def startNewGameDialog(self):
        dialog = NewGameDialog(self.points, self)
        success = dialog.exec_()
        if success:
            self.on_actionNeues_Spiel_triggered()

    @pyqtSignature("")
    def on_actionSchlie_en_triggered(self):
        sys.exit()
