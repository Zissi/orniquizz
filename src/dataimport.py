import os

class Birds(object):
    def __init__(self, path_images, path_sounds):
        self.path_images = path_images
        self.path_sounds = path_sounds
        self.extensions = [".jpg", ".tif", ".jpeg"]

    def make_birddic(self):
        birddic = {}
        for name in os.listdir(self.path_images):
            if name == ".nomedia":
                continue
            
            for files in os.listdir(os.path.join("images", name)):
                if os.path.splitext(files)[1] in self.extensions:
                    if name in birddic:
                        birddic[name][0].append(os.path.join("images", name, files))
                    else:
                        birddic[name] = [[os.path.join("images", name, files)]]
    
#        for name in os.listdir(self.path_sounds):
#            if name == ".nomedia":
#                continue
#            
#            for files in os.listdir("audio/" + name):
#                if files.endswith(".mp3"):
#                    if name in birddic:
#                        birddic[name].append("audio/" + name + "/" + files)
#                    else:
#                        birddic[name] = ["audio/" + name + "/" + files]
                        
        if not birddic:
            raise(ValueError("No birds found :("))

        return birddic