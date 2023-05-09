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

class TestImageCollection(unittest.TestCase):
    def testElementFromJson(self):
        jsonPath = "C:/Users/Andreas/Desktop/CP/imageCollection1.txt"
        with open(jsonPath) as f:
            s = f.readlines()

        s = s[0]
        d = json.loads(s)
        print("\n\n json= "+str(d))
        print("filename" in d)
        cpi2 = ImageCollection.elementFromJson(d)

if __name__ == '__main__':
    unittest.main()
