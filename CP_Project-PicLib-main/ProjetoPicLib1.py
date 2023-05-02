import json
from abc import ABC, abstractmethod
import os

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
    def __init__(self, imageFile, exif, metadata):
        self.imageFile = imageFile
        self.exif = exif
        self.metadata = metadata