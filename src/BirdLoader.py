from src.Translator import Translator

import sqlite3
import os
try:
    import cPickle as pickle #Not available on some python distributions
except ImportError:
    import pickle

class BirdLoader(object):
    """Handle loading information about birds"""

    def __init__(self, db="externals/ornidroid/ornidroid/assets/ornidroid.jpg",
                 pickle_name="birds.pkl", extensions=None):
        if extensions is None:
            extensions = [".jpg", ".tif", ".jpeg"]
        self.extensions = extensions
        self.db = db
        self.pickle_name = pickle_name

    def load_birds(self):
        if os.path.exists(self.pickle_name):
            birds = self.birds_from_pkl(self.pickle_name)
        else:
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            birds = self.birds_from_sql(self.db, self.pickle_name,
                                        cursor)
        return birds

    def birds_from_pkl(self, pickle_name):
        with open(pickle_name) as pickleFile:
            return pickle.load(pickleFile)

    def birds_from_sql(self, db, pickle_name, cursor):
        translator = Translator(db)

        birddic = {}
        cursor.execute("SELECT directory_name FROM bird")
        folders = [r[0] for r in cursor.fetchall()]
        for folder in folders:
            birddic[folder] = {"ID":translator.folder_to_id(folder, cursor), "german_Name":translator.translate(folder),
                               "Family":self.folder_to_family(folder, cursor), "Order":self.folder_to_order(folder, cursor),
                               "Scientific_Name":self.folder_to_scientific_name(folder, cursor),
                               "Habitat":self.folder_to_habitat(folder, cursor),
                               "Image":self.folder_to_imagepath(folder),
                               "Audio":self.folder_to_audiopath(folder)}

        with open(pickle_name, "wb") as pickle_file:
            pickle.dump(birddic, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

        return birddic

    def folder_to_family(self, folder, cursor):
        cursor.execute("SELECT scientific_family_fk FROM bird WHERE directory_name =?", (folder,))
        family_id = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM scientific_family WHERE id=?", (family_id,))
        family = cursor.fetchone()[0]
        return family

    def folder_to_order(self, folder, cursor):
        cursor.execute("SELECT scientific_order_fk FROM bird WHERE directory_name =?", (folder,))
        order_id = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM scientific_order WHERE id=?", (order_id,))
        order = cursor.fetchone()[0]
        return order

    def folder_to_scientific_name(self, folder, cursor):
        cursor.execute("SELECT scientific_name FROM bird WHERE directory_name =?", (folder,))
        scientific_name = cursor.fetchone()[0]
        return scientific_name

    def folder_to_habitat(self, folder, cursor):
        cursor.execute("SELECT habitat1_fk FROM bird WHERE directory_name =?", (folder,))
        habitat_id = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM habitat WHERE lang='de' AND id=?", (habitat_id,))
        habitat = cursor.fetchone()[0]
        return habitat

    def folder_to_imagepath(self, folder):
        try:
            for files in os.listdir(os.path.join("externals/ornidroid/ornidroid_images/src_images", folder)):
                if os.path.splitext(files)[1] in self.extensions:
                    return os.path.join("externals/ornidroid/ornidroid_images/src_images", folder, files)
        except OSError:
            pass

    def folder_to_audiopath(self, folder):
        try:
            for files in os.listdir(os.path.join("externals/ornidroid/ornidroid_audio/src_audio", folder)):
                if files.endswith(".mp3"):
                    return os.path.join("externals/ornidroid/ornidroid_audio/src_audio", folder, files)
        except OSError:
            pass
