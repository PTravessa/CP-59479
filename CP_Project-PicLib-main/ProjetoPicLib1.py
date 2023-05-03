import json
from abc import ABC, abstractmethod
import os

#For exif metadata
from PIL import Image
from PIL.ExifTags import TAGS

class Serializable:
    def toJson(self, classInstance):
        #__dict__ contains attribute values of an object, show as a dictionary
        return classInstance.__dict__
    
    @staticmethod
    @abstractmethod
    def fromJson(dict):
        pass


class CPCollection(Serializable):
    def __init__(self, filename, items):
        self.filename = filename
        self.items = items #A set

    #Adds an item to a collection
    def registerItem(self, item):
        self.items.add(item)

    def saveCollection(self):
        d = self.toJson()
        #Serializing json
        json_object = json.dumps(d, indent=4)
        #Writing to sample .json
        with open(self.filename, "w") as outfile:
            outfile.write(json_object)

    def size(self):
        return len(self.items)

    def toJson(self):
        d = dict(filename=self.filename, items=[item for item in self.items])
        return d
    
    def loadCollection(self):
        with open("C:/Users/Andreas/Desktop/CP/Projeto1/"+self.filename, "r") as openfile:
            json_object = json.load(openfile)

        print(json_object, type(json_object))

    @staticmethod
    @abstractmethod
    def elementFromJson(json):
        pass

#cpCol = CPCollection("C:/Users/Andreas/Desktop/CP/Projeto1/"+"cpColTest.json", {"3boombooms", "Kaligula's friend", 3, "1JohnTron"})
cpCol = CPCollection("cpColTest.json", {"3boombooms", "Kaligula's friend", 3, "1JohnTron"})
cpCol.registerItem("Prroooprpr")


cpCol.loadCollection()


class ImageCollection(CPCollection):
    def __init__(self, filename, items):
        super().__init__(filename, items)

    @staticmethod #Have to add the decorator, bc it doesnt keep super class decorator
    def elementFromJson(json):
        return CPImage.fromJson(json)
    
    #Imports a bunch of files if they're jpg,
    #for every file found, create an CPImage and 
    #add for collection
    def scanFolder(folder):
        files = os.listdir(folder)
        jsonFiles = []
        for file in files:
            if str(file)[-5:-1]+str(file)[-1] == ".json":
                jsonFiles.append(file)
                #Now just make it into a CPImage instance


class CPImage(Serializable):
    def __init__(self, imageFile):
        self.imageFile = imageFile
        self.path = "C://Users//Andreas//Desktop//CP//fotos//AnaLibano"
        image = Image.open(self.path+"//"+self.imageFile)
        if image.getexif() is not None:
            self.exif = image.getexif()
            self.tags = self.getTags()
        #self.metadata = metadata

    def getDate(self):
        return self.tags.get("DateTime")
    
    def getTags(self):
        dict = {}
        for tag_id in self.exif:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = self.exif.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
            dict.update({tag:data})
            # print(f"{tag:25}:{data}")
        return dict
    
    #Nao esta a funcionar
    def setDate(self, date): 
        # self.tags.update({"DateTime": date})#Wrong, only updates the shallow copy dictionary
        for tag_id in self.exif:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = self.exif.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
            if tag == "DateTime":
                data = date
                self.exif.update({"DataTime":date})
                #print(data)
            # print(f"{tag:25}:{data}")
    def get_dimensions(self):
        self.imageFile = Image.open("#path")
        width, height = self.imageFile.size
        dimensions= (width, height)
        return dimensions













