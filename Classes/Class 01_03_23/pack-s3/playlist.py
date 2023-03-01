class PlayList:
    def __init__(self):
        self.musics = []

    def addMusic(self, music):
        self.musics.append(music)

    @classmethod
    def concatenate(cls, list1, list2):
        result = PlayList()
        result.musics = list1.musics + list2.musics
        return result

    def appendMusics(self, other):
        self.musics.extend(other.musics)

    def appendMusics2(self, list1, list2):
        list1.musics.extend(list2.musics)
    
    @classmethod
    def appendMusics3(cls, list1, list2):
        list1.musics.extend(list2.musics)

    # def concatenateBad(self, list1, list2):
    #     result = PlayList()
    #     result.musics = list1.musics + list2.musics
    #     return result


listA = PlayList()
listA.addMusic('music-1')
listA.addMusic('music-2')

listB = PlayList()
listB.addMusic('music-a')
listB.addMusic('music-b') 

listC = PlayList.concatenate(listA,listB)
listD = PlayList.concatenate(listA, listB)

listA.appendMusics(listB)
print(listA.musics)
# print('listaC: ' + str(listC.musics))
# listC.appendMusics2(listA,listB)
# print('listaC: ' + str(listC.musics)) 
print(listA.musics)
PlayList.appendMusics3(listB, listC)

# listB.musics[0] = 'XXXXXX'




