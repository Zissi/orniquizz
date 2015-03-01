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

            
    def get_media(self):
        raise NotImplementedError
    
    def get_answerfolder(self):
        raise NotImplementedError
              
    def translate_answer(self, answerfolder):
        currentbird = self.translator.translate(answerfolder)
        return currentbird #remember to append the birdsplayed list and to save this
                      
    def getfamily_or_order(self, birds, answerfolder, category):
        familyOrder = birds[answerfolder][category]
        samefamilyOrder = []
        for bird in birds:
            if birds[bird][category] == familyOrder and bird != answerfolder:
                samefamilyOrder.append(bird)
        return samefamilyOrder
               
    def get_difficult_answers(self, birds, answerfolder, currentbird):
        samefamily = self.getFamilyorOrder(birds, answerfolder, "Family")   
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
            
 
 
 
 
 
 
 
 
 
        
        
    
    def startQuestion(self):
        raise NotImplementedError
    
    def isCorrect(self):
        return True
    
  