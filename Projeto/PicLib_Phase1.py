from abc import ABC, abstractmethod
import os
import shutil
import json

#For exif metadata
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path


default_folder = input("Enter the path folder for storing imageCollections and CollectionRootFolder, \nLeave as blank to store in default path (Ctr+C to quit): ")
if not os.path.exists(default_folder):
    default_folder = os.getcwd()
    print("Default folder in piclib1 is ",default_folder)

fotoDir = default_folder
collectionDir = default_folder+"/CollectionsRootFolder/"
imageColDir = default_folder+"/ImageCollections/"
defaultCollectionDir = default_folder + '/DefCPCollection'

images = []

if not os.path.isdir(fotoDir):
    os.makedirs(fotoDir)
if not os.path.isdir(collectionDir):    
    os.makedirs(collectionDir)
if not os.path.isdir(imageColDir):    
    os.makedirs(imageColDir)

class Serializable:
    def toJson(self, classInstance):
        #__dict__ contains attribute values of an object, show as a dictionary

        return classInstance.__dict__
    
    @staticmethod
    @abstractmethod
    def fromJson(dict):
        pass


class CPCollection(Serializable):
    def __init__(self, filename, items, dirPath=imageColDir):
        self.filename = filename
        self.dirPath = dirPath
        if (items, '__iter__'): #If argument items is iterable
            self.items = set(items) #A set of all CPImage filenames im guessing
        else:
            self.items = {items}
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
        with open(self.dirPath+"/"+str(self.filename), "w") as outfile:
            outfile.write(s)

    def size(self):
        """Returns the number of items in the collection

        Returns:
            len(self.items)
        """
        return len(self.items)

    def toJson(self, item):
        """Creates and returns a dictionary of an item of the collection

        Args:
            item (Any) 

        Returns:
            _string_: string of a json dictionary
        """
        jsonString = json.dumps(item.__dict__["dirPath"]+item.__dict__["imageFile"])
        l = item.getTagsList()

        return {"Image": [item.__dict__["imageFile"]], "Folder": [item.__dict__["dirPath"]], "tags": l}
    
    @abstractmethod
    def elementFromJson(self, dict):
        pass
    
    def loadCollection(self):
        #with open('C://Users//ASUS//Desktop//Project Pics//'+ self.filename, "r") as openfile:
        """Loads and prints the values of the collection
        Must have a saved collection for it to work 
        """
        with open(self.dirPath+ self.filename, "r") as openfile:
            json_object = json.load(openfile)

        print(json_object, type(json_object))

    @staticmethod
    @abstractmethod
    def elementFromJson(json):
        pass


class ImageCollection(CPCollection):
    def __init__(self, filename, items, dirPath):
        super().__init__(filename, items, dirPath)

    @staticmethod #Have to add the decorator, bc it doesnt keep super class decorator
    def elementFromJson(json):
        """Returns a CPImage

        Args:
            json (_dict_): item.__dict___

        Returns:
            _CPImage_: __
        """
        return CPImage.fromJson(json)
    
    #Imports a bunch of files if they're jpg,
    #for every file found, create an CPImage and 
    #add for collection
    @staticmethod
    def scanFolder(folder):
        """Returns a list of all json files in a folder

        Args:
            folder (str): Path of the folder

        Raises:
            Exception: The folder path does not have json files
        """
        files = os.listdir(folder)
        jsonFiles = []
        for file in files:
            if str(file)[-5:-1]+str(file)[-1] == ".json": #if the last 4 chars are ".json"
                jsonFiles.append(file)
                cpImg = CPImage(file)
                super().registerItem(cpImg)
        if jsonFiles == []:
            raise Exception("No json files found in folder")


    def findWithTag(self, tag):
        """Returns all CPImage Instances with a specified tag

        Args:
            tag (str): Tag of the CPImage instance"""
        imgsWithTag = []
        for cpImg in self.items:
            if tag in cpImg.getTagsList():
                imgsWithTag.append(cpImg)
        return imgsWithTag
    
    @staticmethod
    def allJPGFiles(folder):
        '''
        returns a list of all JPG type files from folder
        '''
        images = os.listdir(folder)
        return [item for item in images if item[-4:] == ".jpg"]
    
class CPImage(Serializable):
    images = []
    def __init__(self, imageFile, dirPath = default_folder):
        """
        CPImage class.
        Args: Filename of the image file.
        """
        self.imageFile = imageFile
        #self.path = 'C://Users//ASUS//Desktop//Project Pics//AnaLibano//P_20201226_145438.jpg'
        self.dirPath = dirPath
        print(self.dirPath)
        path = self.dirPath + "/" + self.imageFile
        path = path.replace("//", "/")
        if path[0] == "/":
            path.removeprefix("/") 
        image = Image.open(path)
        if image.getexif() is not None:
            self.exif = image.getexif()
            self.etags = self.getExifTags()
    
    def getDate(self):
        """
        Gets the date of the image.
        Returns: Date of the image in string format.
        """
        if "DateTimeOriginal" in self.etags:
            return self.etags.get("DateTimeOriginal")
        elif "DateTime" in self.etags:
            return self.etags.get("DateTime")
        elif "DateTimeDigitized" in self.etags:
            return self.etags.get("DateTimeDigitized")
        else:
            print("No DateTimeOriginal, DateTime or DateTimeDigitized key in exif tags")
            return ""

    def getExifTags(self):
        """
        Gets the EXIF tags of the image.
        Returns: Dictionary (dict) containing the EXIF tags and their values.
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

    @staticmethod
    def getAllImages(dirPath):
        """Finds all jpg and png files in a folder and makes a list of CPImage instances of it
    
        Includes CPImage instances of files in subfolders in folder

        Args:
            dirPath (str): path of the folder
        """
        CPImage.images = []
        for root, dirs, files in os.walk(dirPath):
            for filename in files:
                fullPath = os.path.join(root, filename)
                if filename.endswith('.png') or filename.endswith('.jpg'):
                    CPImage.images.append(fullPath)
        return CPImage.images

    
    @staticmethod
    def makeAllCPImages(dirPath, newDirPath):
        """Creates an album of the images 

        For each image, creates 3 subfolders representing its year, month and day, in day a copy of the original image is stored. All is stored in newDirPath.
        
        Includes images in subfolders of the dirPath

        Args:
            dirPath (str): Path of the folder
            newDirPath (_type_): Path of the album folder
        """
        images = CPImage.getAllImages(dirPath)
        counter = 0
        for image in images:
            filename = str(image.split(os.sep)[-1])
            foldername = os.sep.join(image.split(os.sep)[:-1])
            a = CPImage.makeCPImage(filename, foldername, newDirPath)
            print("COUNTER =", counter)
            print("Date cpimage is", a.getDate())
            counter += 1

    @staticmethod
    def makeCPImage(filename, dir_path, newDirPath):
        """Creates a CPImage instance of an image file

        Stores a copy of the image in folder newDirPath, and creates 3 subfolders as newDirPath/year/month/day/imageCopy

        Args:
            filename (str): Name of the file
            dir_path (str): Path of the folder the file is stored in
            newDirPath (_type_): Path of the folder to store a copy of the image

        Returns:
            CPImage: CPImage instance of the new image file
        """
        if not os.path.exists(os.path.join(dir_path, filename)):
            print("The image has to exist in the specified folder")
            return None

        cpImage = CPImage(filename, dir_path)
        date = cpImage.getDate()

        if date == "":
            newPath = Path(newDirPath) / "No date"
            if not newPath.is_dir():
                print("newPath is", newPath)
                newPath.mkdir(parents=True)

            newFilePath = newPath / cpImage.imageFile
            if not newFilePath.is_file():
                shutil.copy(os.path.join(cpImage.dirPath, cpImage.imageFile), newFilePath)
            else:
                print("Image file already in folder")

            return CPImage(cpImage.imageFile, str(newPath))

        date = date.split(":")
        year = date[0]
        month = date[1]
        day = date[2].split(" ")[0]

        folder_path = newDirPath
        directoryPaths = [x[0] for x in os.walk(os.path.join(folder_path, year))]
        fileNames = [x.split(os.sep)[-1] for x in directoryPaths]
        newPath = os.path.join(folder_path, year, month, day)

        print(fileNames)
        print(year)
        if not os.path.isdir(newPath):
            print("newPath is", newPath)
            os.makedirs(newPath)

        newFilePath = os.path.join(newPath, cpImage.imageFile)
        if not os.path.isfile(newFilePath):
            shutil.copy(os.path.join(cpImage.dirPath, cpImage.imageFile), newFilePath)
        else:
            print("Image file already in folder")

        return CPImage(cpImage.imageFile, newPath)

    def copyToFolder(self, folder_path= default_folder + '/collectionsRootFolder'):
        """
        Copies the image to the folder.
        """
        date = self.getDate()
        date = date.split(":")
        year = date[0]
        #List of the names of sub folders of album 
        directoryPaths = [x[0] for x in os.walk(folder_path+"/"+year)]
        print(directoryPaths)
        fileNames = [x.split("/")[-1] for x in directoryPaths] 
        newPath = folder_path+"/"+year
        print(fileNames)
        print(year)
        if year not in fileNames: #If there is no year album, create one
            os.mkdir(newPath)
        if not os.path.isfile(newPath+"/"+self.imageFile): 
            shutil.copy(self.dirPath+"/"+self.imageFile, newPath+"/"+self.imageFile)
        else:
            print("Image file already in folder")
        

        # shutil.copy(self.path + "//" + self.imageFile, folder_path)
    
    def setDate(self, date):
        """
        Sets the date of the image in string format.
        Args: date in str "2000:10:23 07/07/30"

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
            image = Image.open(self.dirPath+"/collectionsRootFolder/"+self.imageFile)
            i = etag.index("DateTimeOriginal")

            self.exif[etagId[i]] = date
            # print("On datetimeog")
            image.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
            image.close()
        elif "DateTime" in etag:
            image = Image.open(self.dirPath+"/"+self.imageFile)
            i = etag.index("DateTime")
            self.exif[etagId[i]] = date
            # print("On datetime")
            image.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
            image.close()
        elif "DateTimeDigitized" in etag:
            image = Image.open(self.dirPath+"/"+self.imageFile)
            i = etag.index("DateTimeDigitized")
            self.exif[etagId[i]] = date
            # print("On datetime")
            image.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
            image.close()

        else:
            # image = Image.open(self.dirPath+"/"+self.imageFile)
            # i = etag.index("DateTime")
            # self.exif[etagId[i]] = date
            # # print("On datetime")
            # image.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
            # image.close()

            img = Image.open(self.dirPath+"/"+self.imageFile)
        
            TAG_ID = 0x0132
            if "DateTime" not in etag:
                tempD = {TAG_ID: date}
                self.exif[TAG_ID] = json.dumps(tempD[TAG_ID], ensure_ascii=False)
                self.exif[TAG_ID] = str(self.exif[TAG_ID]).replace("\"", "")
                img.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
                img.close()
    
    def getImageFile(self):
        """
        Gets the name of the image file.
        """
        return self.imageFile


    def get_dimensions(self):
        """
        Gets the dimensions of the image.
        Returns: Tuple containing the width and height of the image.
        """
        image_path = self.dirPath + '/' + self.imageFile
        with Image.open(image_path) as img:
            width, height = img.size
        return (width, height)
    
    @staticmethod
    def fromJson(jsonDict):
        if "filename" in jsonDict:
            return CPImage(jsonDict["filename"])
        cpImage = CPImage(jsonDict[0])

    def toJson(self, filename): 
        etag = [] 
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
        return {"filename": self.imageFile, "tags": l}


    def addTag(self, tag):
        """
        Adds a tag string to the exif metadata of the image.
        """
        if tag == "":
            print("Error: Tag can't be an empty string")
            return  
        
        etag = []  # tag dos metadados, nao relacionados a classe tag
        etagId = []
        try:
            for etag_id in self.exif:
                etag.append(TAGS.get(etag_id, etag_id))
                etagId.append(etag_id)
        except ValueError as e:
            print("Error:", str(e))
            return  

        img = Image.open(self.dirPath+"/"+self.imageFile)
        
        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        allTags = self.getExifTags()
        if "Tags" not in etag:
            tempD = {TAG_ID: tag}
            self.exif[TAG_ID] = json.dumps(tempD[TAG_ID], ensure_ascii=False)
            img.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
            img.close()
        if "Tags" in etag:
            if not self.hasTag(tag):
                TAG_ID = 4660
                tempD = self.exif[TAG_ID]
                s = json.dumps(str(self.exif[TAG_ID]) +", "+str(tag), ensure_ascii=False)
                s=str(s).replace("\\", "")
                s=str(s).replace("\"", "")

                self.exif[TAG_ID] = s
                img.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
                img.close()

    def removeTag(self, tag): 
        """
        Removes a tag string from the exif metadata of the image.
        """ 
        etag = [] 
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            etagId.append(etag_id)

        img = Image.open(self.dirPath+"/"+self.imageFile)
        
        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        allTags = self.getExifTags()

        if "Tags" in etag:
            if self.hasTag(tag):
                TAG_ID = 4660
                tempD = self.exif[TAG_ID]
                tl = self.getTagsList()
                tl.remove(tag)
                s = ", ".join(tl)
                s = json.dumps(s, ensure_ascii=False)#str(tl, ensure_ascii=False)

                self.exif[TAG_ID] = s
                img.save(self.dirPath+"/"+self.imageFile, exif = self.exif)
                img.close()
            else:
                print("Tag is not in image Tags")
        else:
            print("No Exif tag name \"Tag\" in exif metadata")

    def hasTag(self, tag):
        """
        Args: tag (_str_)
        Returns: _bool_
        """
        etag = [] 
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
        """Returns the tags in a string"""
        etag = [] 
        etagId = []
        for etag_id in self.exif:
            etag.append(TAGS.get(etag_id, etag_id))
            etagId.append(etag_id)

        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        if TAG_ID in self.exif:
            return self.exif[TAG_ID]
        else: 
            return ""
        
    def getTagsList(self):
        """Returns a list of the tags as strings"""
        TAG_ID = 4660
        TAGS[TAG_ID] = "Tags"
        if TAG_ID in self.exif:
            tags = self.getTags()
            tags = tags.replace("\"", "")

            l = tags.split(", ")
            return l
        else:
            return []
        
    @staticmethod
    def countFilesInFolders(folder_path):
        """Returns the number of png and jpg files in folder with sub-folders

        Args:
            folder_path (str)

        Returns:
            _int_: number of files
        """
        for filename in os.listdir(folder_path):
            fullPath = folder_path +"/"+ filename
            if filename.endswith('.png') or filename.endswith('.jpg'):
                images.append(fullPath)
            elif os.path.isdir(fullPath):
                CPImage.countFilesInFolders(fullPath)
        return len(images)

        
class Tag(Serializable):
    def __init__(self, name):
        self.name = name


# Define a new tag ID for the "SomethingNew" tag
TAG_ID = 0x1234
# Add the new tag to the TAGS dictionary
TAGS[TAG_ID] = "Tags"
# Look up the tag ID for the "SomethingNew" tag
new_tag_id = TAGS.get("Tags")


CPImage.makeAllCPImages(fotoDir, collectionDir)
print(CPImage.countFilesInFolders(collectionDir))

print("Default folder is ", default_folder)