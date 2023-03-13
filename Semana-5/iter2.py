class SpecialList:

    def __init__(self):
        self.content = []
        self.position = None

    def add(self, e):
        self.content.append(e)

    def len(self):
        return len(self.content)

    def select(self, position):
        self.selected = position
    
    def getSelected(self):
        return self.content[self.selected]

    def __iter__(self):
        return self.SpecialListIter(self.content)

    class SpecialListIter:
        def __init__(self, elements):
            self.current = 0
            self.elements = elements
            self.nelements = len(elements)

        def __next__(self):
            self.current = self.current + 1
            if self.current <= self.nelements:
                return self.elements[self.current - 1]
            else: 
                raise StopIteration

        def hasNext(self):
            return self.current < self.nelements
 
# testing
special = SpecialList()
special.add(888) 
special.add('Ola')
special.add('Ole')

for thing in special:
    print(thing)
