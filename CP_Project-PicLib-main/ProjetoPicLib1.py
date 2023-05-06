import json
from abc import ABC, abstractmethod
import os

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
            self.etags = self.getExifTags()
    
    def getDate(self):
        """
        Gets the date of the image.
        Returns: Date of the image in string format.
        """
        return self.etags.get("DateTime")

    def getExifTags(self):
        """
        Gets the EXIF tags of the image.
        Returns: Dictionary containing the EXIF tags and their values.
        """
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
    


    def get_dimensions(self):
        """
        Gets the dimensions of the image.
        Returns: Tuple containing the width and height of the image.
        """
        image_path = self.path + '/' + self.imageFile
        with Image.open(image_path) as img:
            width, height = img.size
        return (width, height)
    
    @staticmethod
    def fromJson(jsonDict):
        #I think jsonDict[0] will be a filename
        cpImage = CPImage(jsonDict[0])

    def addTag(self, tag):
        """
        Adds a tag string to the exif metadata of the image.

        """ 
        etag = [] #tag dos metadados, nao relacionados a classe tag
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            etagId.append(etag_id)

        if "Tag" in etag:
            image = Image.open(self.path+"//"+self.imageFile)
            i = etag.index("Tag")
            # Look up the tag ID for the "somethingNew" tag, or use a default value of -1 if it doesn't exist
            new_tag_id = TAGS.get('Tag', -1)

            # Print the tag ID
            # print(new_tag_id)

            # self.exif[i] = tag
            # image.save(self.path+"//"+self.imageFile, exif = self.exif)
            exif_dict = piexif.load(image.info["exif"])

            # Define the new Exif tag ID and name
            TAG_ID = 0x1234
            TAG_ID = int(TAG_ID)
            TAG_NAME = "Tag"

            # # # Add the new Exif tag with the desired value to the Exif data dictionary
            # exif_dict["Exif"][TAG_ID] = "my_new_value"
            self.exif[TAG_ID] = tag


            # Convert the Exif data dictionary back to bytes and update the image's Exif data
            exif_bytes = piexif.dump(self.exif)
            image.save(self.path+"/"+self.imageFile, "jpeg", exif=self.exif)


        else:
            image = Image.open(self.path+"//"+self.imageFile)
            # Look up the tag ID for the "Tag" tag, or use a default value of -1 if it doesn't exist
            new_tag_id = TAGS.get('Tag', -1) #TAG_ID 0x1234
            
            # self.exif[new_tag_id] = tag
            # # print(self.exif)
            # # print("Them exif tags "+str(self.getExifTags()))
            # # print(TAGS.get(new_tag_id, new_tag_id))
            # image.save(self.path+"//"+self.imageFile, exif = self.exif)            
    
            exif_dict = piexif.load(image.info["exif"])

            # Define the new Exif tag ID and name
            TAG_ID = 0x1234
            TAG_ID = int(TAG_ID)
            TAG_NAME = "Tag"

            # # # Add the new Exif tag with the desired value to the Exif data dictionary
            self.exif[TAG_ID] = tag

            # Convert the Exif data dictionary back to bytes and update the image's Exif data
            # exif_bytes = piexif.dump(exif_dict)
            image.save(self.path+"/"+self.imageFile, "jpeg", exif=self.exif)



class Tag(Serializable):
    def __init__(self, name):
        self.name = name


# Define a new tag ID for the "SomethingNew" tag
TAG_ID = 0x1234
# Add the new tag to the TAGS dictionary
TAGS[TAG_ID] = "Tag"
# Look up the tag ID for the "SomethingNew" tag
new_tag_id = TAGS.get("Tag")
# Print the tag ID
print(new_tag_id)


image1 = CPImage("P_20200722_202131.jpg")
print("Dimensions: "+str(image1.get_dimensions()))
print("Original date"+str(image1.getDate())) #2016:08:12 20:07:18
print("BEFORE Exif tags dict: "+str(image1.getExifTags()))
print("BEFORE Exif dict: "+str(image1.exif))

image1.setDate("2000:02:15 23:35:42")
print("New date (may have to run again to see change though) "+image1.getDate())
print("Exif tags dict: "+str(image1.getExifTags()))
print("Exif dict: "+str(image1.exif))
print("\n add Tag TestTag \n print(image1.exif)")
image1.addTag("TestTag")
print("image1.exif "+str(image1.exif))
print("image1.getExifTags() "+str(image1.getExifTags()))







