'''
Created on 09.02.2014

@author: zissi
'''
import sqlite3
import os

class Translator(object):
    '''
    classdocs
    '''


    def __init__(self, db):
        connection = sqlite3.connect(db)
        self.cursor = connection.cursor()
        self.extensions = [".jpg", ".tif", ".jpeg"]
        
    def folderToId(self, folder):
        self.cursor.execute("SELECT id FROM bird WHERE directory_name=?", (folder,))
        try:
            bird_id = self.cursor.fetchone()[0]
        except:
            bird_id = None
        return bird_id
        
    def translate(self, folder):
        bird_id = self.folderToId(folder)
        if bird_id is None:
            return folder
        self.cursor.execute("SELECT c1taxon FROM taxonomy_content WHERE c0lang='de' AND c3bird_fk=?", (bird_id,))
        gername = self.cursor.fetchone()[0]
        return gername
    
    def folderToFamily(self, folder):
        self.cursor.execute("SELECT scientific_family_fk FROM bird WHERE directory_name =?", (folder,))
        family_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT name FROM scientific_family WHERE id=?", (family_id,))
        family = self.cursor.fetchone()[0]
        return family

    def folderToOrder(self, folder):
        self.cursor.execute("SELECT scientific_order_fk FROM bird WHERE directory_name =?", (folder,))
        order_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT name FROM scientific_order WHERE id=?", (order_id,))
        order = self.cursor.fetchone()[0]
        return order
    
    def folderToScientificName(self, folder):
        self.cursor.execute("SELECT scientific_name FROM bird WHERE directory_name =?", (folder,))
        scientific_name = self.cursor.fetchone()[0]
        return scientific_name
    
    def folderToHabitat(self, folder):
        self.cursor.execute("SELECT habitat1_fk FROM bird WHERE directory_name =?", (folder,))
        habitat_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT name FROM habitat WHERE lang='de' AND id=?", (habitat_id,))
        habitat = self.cursor.fetchone()[0]
        return habitat
    
    def folderToImagepath(self, folder):
        try:
            for files in os.listdir(os.path.join("externals/ornidroid/ornidroid_images/src_images", folder)):
                if os.path.splitext(files)[1] in self.extensions:
                    return os.path.join("externals/ornidroid/ornidroid_images/src_images", folder, files)
        except OSError:
            pass
        
    def folderToAudiopath(self, folder):
        try:
            for files in os.listdir(os.path.join("externals/ornidroid/ornidroid_audio/src_audio", folder)):
                if files.endswith(".mp3"):
                    return os.path.join("externals/ornidroid/ornidroid_audio/src_audio", folder, files)
        except OSError:
            pass
        
    
    def createBirddic(self):
        birddic = {}
        self.cursor.execute("SELECT directory_name FROM bird")
        folders = [r[0] for r in self.cursor.fetchall()]
        for folder in folders:
            birddic[folder] = {"ID" : self.folderToId(folder), "german_Name" : self.translate(folder), "Family" : self.folderToFamily(folder), "Order" : self.folderToOrder(folder),
                               "Scientific_Name" : self.folderToScientificName(folder), "Habitat" : self.folderToHabitat(folder), "Image" : self.folderToImagepath(folder), "Audio" : self.folderToAudiopath(folder)}
        return birddic
            

        
