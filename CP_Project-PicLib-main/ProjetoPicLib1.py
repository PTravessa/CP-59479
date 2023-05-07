import json
from abc import ABC, abstractmethod
import os
import shutil

#For exif metadata
from PIL import Image
from PIL.ExifTags import TAGS
import piexif #For adding a new tag to a jpg's exif

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
        if (items, '__iter__'): #If argument items is iterable
            self.items = set(items) #A set of all CPImage filenames im guessing
        else:
            self.items = {items}

    #Adds an item to a collection
    def registerItem(self, item):
        self.items.add(item)

    def saveCollection(self):
        """
        Saves the items in a file self.filename
        """
        l = []
        for item in self.items:
            item = self.toJson(item) #Nao modifica self.items, copia e modifica a copia
            l.append(item)
        
        d = {"filename": self.filename, "items": l}
        print("The dict list is "+str(d))
        s = json.dumps(d)
        with open(self.filename, "w") as outfile:
            outfile.write(s)

    def size(self):
        return len(self.items)

    def toJson(self, item):
        # d = dict(filename=self.filename, items=[item for item in self.items])
        # jsonItem = json.dumps(item, ensure_ascii=False)
        jsonString = json.dumps(item.__dict__["imageFile"])
        return {"Image": item.__dict__["imageFile"]}
    
    @abstractmethod
    def elementFromJson(self, dict):
        pass
    
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
cpCol = CPCollection("cpColTest.json", ["3boombooms", "Kaligula's friend", 3, "1JohnTron"])
cpCol.registerItem("Prroooprpr")


cpCol.loadCollection()


class ImageCollection(CPCollection):
    def __init__(self, filename, items):
        super().__init__(filename, items)

    @staticmethod #Have to add the decorator, bc it doesnt keep super class decorator
    def elementFromJson(json):
        """Returns a CPImage

        Args:
            json (_dict_): _item.__dict___

        Returns:
            _CPImage_: __
        """
        return CPImage.fromJson(json)
    
    #Imports a bunch of files if they're jpg,
    #for every file found, create an CPImage and 
    #add for collection
    def scanFolder(folder):
        files = os.listdir(folder)
        jsonFiles = []
        for file in files:
            if str(file)[-5:-1]+str(file)[-1] == ".json": #if the last 4 chars are ".json"
                jsonFiles.append(file)
                cpImg = CPImage(file)
                super().registerItem(cpImg)


class CPImage(Serializable):
    def __init__(self, imageFile, path):
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
            self.etags = self.getTags()
    
    def getDate(self):
        """
        Gets the date of the image.
        Returns: Date of the image in string format.
        """
        if "DateTimeOriginal" in self.etags:
            return self.etags.get("DateTimeOriginal")
        elif "DateTime" in self.etags:
            return self.etags.get("DateTime")
        else:
            print("No DateTimeOriginal or DateTime key in exif tags")

    def getExifTags(self):
        """
        Gets the EXIF tags of the image.
        Returns: Dictionary containing the EXIF tags and their values.
        """
        # Define the new Exif tag ID and name
        TAG_ID = 0x1234
        TAG_ID = int(TAG_ID)
        
        dict = {}
        for etag_id in self.exif: #etag as in exifTags
            etag = TAGS.get(etag_id, etag_id)
            data = self.exif.get(etag_id)
            if isinstance(data, bytes):
                data = data.decode()
            dict.update({etag: data})
        
        return dict

    
    def setDate(self, date):
        """
        Sets the date of the image in string format.

        """ 
        # Define the new Exif tag ID and name
        TAG_ID = 0x1234
        TAG_ID = int(TAG_ID)
        etag = [] #tag dos metadados, nao relacionados a classe tag
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            # print("etag_id "+str(etag_id)+" Tags.get... "+str(TAGS.get(etag_id, etag_id)))
            etagId.append(etag_id)

        if "DateTimeOriginal" in etag:
            image = Image.open(self.path+"//"+self.imageFile)
            i = etag.index("DateTimeOriginal")

            self.exif[etagId[i]] = date
            # print("On datetimeog")
            image.save(self.path+"//"+self.imageFile, exif = self.exif)
        elif "DateTime" in etag:
            image = Image.open(self.path+"//"+self.imageFile)
            i = etag.index("DateTime")
            self.exif[etagId[i]] = date
            # print("On datetime")
            image.save(self.path+"//"+self.imageFile, exif = self.exif)
    
    def getImagefile(self):
        """
        Gets the name of the image file.
        """
        return self.imageFile


    def get_dimensions(self):
        """
        Gets the dimensions of the image.
        Returns: Tuple containing the width and height of the image.
        """
        image_path = self.path + '/' + self.imageFile
        with Image.open(image_path) as img:
            width, height = img.size
        return (width, height)
    
    def getImageFile(self):
        return self.imageFile
    
    @staticmethod
    def fromJson(jsonDict):
        #I think jsonDict[0] will be a filename
        if "imageFile" in jsonDict:
            return CPImage(jsonDict["imageFile"])
        cpImage = CPImage(jsonDict[0])

    #toJson() Ja definido no Serializable
    def toJson(self, filename): 
        return {"filename": self.imageFile}

    def copyToFolder(self, folder_path):
        """
        Copies the image to the given folder.
        """
        image_path = self.path + '/' + self.imageFile
        try:
            shutil.copy(image_path, folder_path)
            return "File copied and located in {}".format(folder_path)
        except Exception as error:
            return "Error copying file: {}".format(str(error))


    #Tentei mas nao funciona
    def addTag(self, tag): 
        """
        Adds a tag string to the exif metadata of the image.
        """ 
        etag = [] #tag dos metadados, nao relacionados a classe tag
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            etagId.append(etag_id)

        # Open the image file
        img = Image.open(self.path+"/"+self.imageFile)
        
        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        allTags = self.getExifTags()
        if "Tags" not in etag:
            tempD = {TAG_ID: tag}
            self.exif[TAG_ID] = json.dumps(tempD[TAG_ID], ensure_ascii=False)
            img.save(self.path+"//"+self.imageFile, exif = self.exif)
            img.close()
        if "Tags" in etag:
            if not self.hasTag(tag):
                TAG_ID = 4660
                # tempD = {TAG_ID: self.exif[TAG_ID] +(3,)}
                tempD = self.exif[TAG_ID]
                # self.exif[TAG_ID] = json.dumps(self.exif[TAG_ID] +str({s:tag},))
                s = json.dumps(str(self.exif[TAG_ID]) +", "+str(tag), ensure_ascii=False)
                s=str(s).replace("\\", "")
                s=str(s).replace("\"", "")

                # self.exif[TAG_ID] = json.dumps(self.exif[TAG_ID] +", "+str(tag))
                self.exif[TAG_ID] = s
                # print("json.dumps(tempD[TAG_ID]) = " + str(json.dumps(tempD[TAG_ID])))
                img.save(self.path+"//"+self.imageFile, exif = self.exif)
                img.close()

    def hasTag(self, tag):
        """
        Args: tag (_str_)
        Returns: _bool_
        """
        etag = [] #tag dos metadados, nao relacionados a classe tag
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            etagId.append(etag_id)

        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        if TAG_ID in self.exif:
            tags = self.getTags()
            tags = tags.replace("\"", "")

            l = tags.split(", ")
            if tag in l:
                return True
        return False
    
    def getTags(self):
        etag = [] #tag dos metadados, nao relacionados a classe tag
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            etagId.append(etag_id)

        # Open the image file
        img = Image.open(self.path+"/"+self.imageFile)
        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        if TAG_ID in self.exif:
            return self.exif[TAG_ID]
        else: 
            return ""
        
class Tag(Serializable):
    def __init__(self, name):
        self.name = name


# Define a new tag ID for the "SomethingNew" tag
TAG_ID = 0x1234
# Add the new tag to the TAGS dictionary
TAGS[TAG_ID] = "Tags"
# Look up the tag ID for the "SomethingNew" tag
new_tag_id = TAGS.get("Tags")

path = "C://Users//Andreas//Desktop//CP//fotos//AnaLibano" # Path Andreas
#path = "C://Users//ASUS//Desktop//Project Pics//AnaLibano" # Path PTravessa
import os
# assign directory
 
# iterate over files in
# that directory
fl = []
for filename in os.listdir(path):
    f = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # print(filename)
        fl.append(filename)

image1 = CPImage(fl[16], path)
image1.addTag("TestTag1")
img2 = CPImage(fl[2], path)
img2.addTag("TestTag5")

print("\n "+str(image1.__dict__))

#TAG Testing
print("image1.hasTag(\"TestTag1\")" + str(image1.hasTag("TestTag1")))
print("image1.getTags() ")
print(image1.getTags())
print("\n image exif tags "+str(image1.getTags()))

print("\n\n IMG1.__dict__ "+str(image1.__dict__))
print("\n\n IMG2.__dict__ "+str(img2.__dict__))

#ImageCollection Testing
imgCol = ImageCollection("imageCollection1.txt", [image1])
imgCol.registerItem(img2)

imgCol.saveCollection()