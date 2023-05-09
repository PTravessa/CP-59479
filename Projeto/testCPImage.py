import unittest
import os
import json
from ProjetoPicLib1 import CPImage, ImageCollection, CPCollection, Tag

# iterate over files in
# that directory
path = "C://Users//Andreas//Desktop//CP//fotos//AnaLibano"
fl = []
for filename in os.listdir(path):
    f = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # print(filename)
        fl.append(filename)

cpi1 = CPImage(fl[0], path)
class TestCPImageMethods(unittest.TestCase):
    def testSetDate(self):
        cpi1 = CPImage(fl[0], path)
        date = "1999:05:05 23:10:5"
        cpi1.setDate(date)
        self.assertEqual(date, cpi1.getDate())

    def testGetImageFile(self):
        nameOfFile = "monumento.jpg"
        cpi2 = CPImage("monumento.jpg", "C:/Users/Andreas/Desktop/CP/fotos/AracyBettencourt")
        self.assertEqual(nameOfFile, cpi2.getImageFile())

    def testAddTag(self):
        tag = "A new test tag"
        cpi1.addTag(tag)
        self.assertTrue(tag in cpi1.getTagsList())
        self.assertTrue(cpi1.hasTag(tag))

    #testRemoveTag tambem testa o CPImage.hasTag()
    def testRemoveTag(self):
        tag = "Tag to remove" #Same as before to test if it gets removed 
        cpi1.addTag(tag)
        print(cpi1.getTags())
        self.assertTrue(cpi1.hasTag(tag))
        cpi1.removeTag(tag)
        print(cpi1.getTags())
        self.assertFalse(cpi1.hasTag(tag))





if __name__ == '__main__':
    unittest.main()
