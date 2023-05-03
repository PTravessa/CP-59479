import datetime


class Ad:
    def __init__(self, author, publicationDate, item, transactionType):
        self.author = author
        self.publicationDate = publicationDate
        self.item = item
        self.transactionType = transactionType

    def getAge(self):
        return datetime.datetime.now() - self.publicationDate

    def getItem(self):
        return self.item

    def getPublicationDate(self):
        return self.publicationDate

    def isActive(self):
        return self.getAge() < datetime.timedelta(days=15)


class CarAd(Ad):

    def __init__(self, author, publicationDate, item, transactionType,
                 brand, model, year, km, state):
        super().__init__(author, publicationDate, item, transactionType)
        self.brand = brand
        self.model = model
        self.year = year
        self.km = km
        self.state = state

    def setState(self, newState):
        self.state = newState

    def getState(self):
        return self.state

