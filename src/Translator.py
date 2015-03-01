'''
Created on 09.02.2014

@author: zissi
'''
import sqlite3

class Translator(object):
    """Handle the sqlite database."""

    def __init__(self, db="externals/ornidroid/ornidroid/assets/ornidroid.jpg"):
        connection = sqlite3.connect(db)
        self.cursor = connection.cursor()

    def translate(self, folder):
        bird_id = self.folder_to_id(folder, self.cursor)
        if bird_id is None:
            return folder
        self.cursor.execute("SELECT c1taxon FROM taxonomy_content WHERE c0lang='de' AND c3bird_fk=?", (bird_id,))
        gername = self.cursor.fetchone()[0]
        return gername

    def folder_to_id(self, folder, cursor):
        cursor.execute("SELECT id FROM bird WHERE directory_name=?", (folder,))
        try:
            bird_id = cursor.fetchone()[0]
        except:
            bird_id = None
        return bird_id
