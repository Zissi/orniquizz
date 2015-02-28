'''
Created on 02.03.2014

@author: zissi
'''
import random, os
from PyQt4.QtCore import pyqtSignature, Qt
from Translator import Translator

class Quiz(object):
    
    def __init__(self, parent=None):
        self.wrongAnswers = []
        self.answerfolder = None
        self.currentbird = None
        self.turns = 0
        
        
    @pyqtSignature("")        
    def startQuestion(self, Gamemode, Difficulty):
        self.resetForNewQuestion()
        
        if Gamemode == "Both":
            self.getAnswerBothquiz()
        else:
            self.getAnswerSinglequiz(self.GameMode)
            
        self.get_media()
        
        self.saveCurrentAnswer()
        
        if Difficulty == "Hard":
            self.getDifficultAnswers()    
        elif self.Difficulty == "Intermediate":
            self.getIntermediateAnswer()
        else:
            self.getEasyAnswer()
         
        self.combineAnswers()
        self.makeButtons()
        
    def resetForNewQuestion(self):
        self.turns += 1
        self.bild1.setToolTip("") 
        for button in self.buttons:
            button.setStyleSheet("")
            button.setEnabled(True)
                            
    def getAnswerBothquiz(self):
        data = False
        while data == False:
            self.answerfolder = random.sample(self.birds, 1)[0]
            if self.birds[self.currentfolder][str("Audio")] is not None and self.birds[self.currentfolder][str("Image")] is not None:
                data = True 
        return self.currentfolder
            
    def get_media(self):
        raise NotImplementedError
    
    def get_answerfolder(self):
        raise NotImplementedError
              
    def translate_answer(self):
        self.currentbird = self.translator.translate(self.answerfolder)
        return self.currentbird 
                      
    def getfamily_or_order(self, birds, category):
        familyOrder = birds[self.answerfolder][category]
        samefamilyOrder = []
        for bird in birds:
            if birds[bird][category] == familyOrder and bird != self.answerfolder:
                samefamilyOrder.append(bird)
        return samefamilyOrder
               
    def get_difficult_answers(self, birds):
        samefamily = self.getFamilyorOrder(birds, self.answerfolder, "Family")   
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
        self.wrongAnswers = randomlist
        return randomlist
           
    def get_intermediate_answers(self, birds):
        sameorder = self.getFamilyorOrder("Order")
        try:
            randomlist = random.sample(sameorder, 3)
        except ValueError:
            randomlist = random.sample(sameorder, len(sameorder))
            randomlist = randomlist + random.sample(birds, 3 - len(sameorder))
        self.wrongAnswers = randomlist
        return self.wrongAnswers
       
    def get_easy_answers(self, birds):
        randomlist = random.sample(birds, 3)
        self.wrongAnswers = randomlist
        return randomlist
    
    def combine_answers(self):
        self.wrongAnswers.append(self.answerfolder)
        allAnswers = random.shuffle(self.wrongAnswers)
        return allAnswers
                
    def makeButtons(self):
        for idx, button in enumerate(self.buttons):
            gername = self.translator.translate(self.wrongAnswers[idx])
            button.setText(gername)
            
    
  