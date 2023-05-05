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
        #with open('C://Users//ASUS//Desktop//Project Pics//'+ self.filename, "r") as openfile:
        with open('C:/Users/Andreas/Desktop/CP/Projeto1/'+ self.filename, "r") as openfile:
            json_object = json.load(openfile)

        print(json_object, type(json_object))

    @staticmethod
    @abstractmethod
    def elementFromJson(json):
        pass

#cpCol = CPCollection("'C://Users//ASUS//Desktop//Project Pics//AnaLibano//P_20201226_145438.jpg'"+"cpColTest.json", {"3boombooms", "Kaligula's friend", 3, "1JohnTron"})
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
        """
        CPImage class.
        Args: Filename of the image file.
        """
        self.imageFile = imageFile
        #self.path = 'C://Users//ASUS//Desktop//Project Pics//AnaLibano//P_20201226_145438.jpg'
        self.path = 'C://Users//Andreas//Desktop//CP//fotos//AnaLibano'
        image = Image.open(self.path + "//" + self.imageFile)
        if image.getexif() is not None:
            self.exif = image.getexif()
            self.tags = self.getTags()
    
    def getDate(self):
        """
        Gets the date of the image.
        Returns: Date of the image in string format.
        """
        return self.tags.get("DateTime")

    def getTags(self):
        """
        Gets the EXIF tags of the image.
        Returns: Dictionary containing the EXIF tags and their values.
        """
        dict = {}
        for tag_id in self.exif:
            tag = TAGS.get(tag_id, tag_id)
            data = self.exif.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            dict.update({tag: data})
        return dict

    
    def setDate(self, date):
        """
        Sets the date of the image in string format.

        """ 
        for tag_id in self.exif:
            image = Image.open(self.path+"//"+self.imageFile)
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                self.exif[tag_id] = date
                image.save(self.path+"//"+self.imageFile, exif = self.exif)
                break
            if tag == "DateTime":
                self.exif[tag_id] = date
                image.save(self.path+"//"+self.imageFile, exif = self.exif)
                break
    


    def get_dimensions(self):
        """
        Gets the dimensions of the image.
        Returns: Tuple containing the width and height of the image.
        """
        image_path = self.path + '/' + self.imageFile
        with Image.open(image_path) as img:
            width, height = img.size
        return (width, height)



image1 = CPImage("IMG_20160812_200717168_HDR.jpg")
print("Dimensions: "+str(image1.get_dimensions()))
print("Original date"+image1.getDate()) #2016:08:12 20:07:18
image1.setDate("2000:02:15 14:05:10")
print("New date (may have to run again to see change though) "+image1.getDate())












