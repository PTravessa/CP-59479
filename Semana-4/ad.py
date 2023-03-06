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
        self.state = state

    def setState(self, newState):
        self.state = newState

    def getState(self):
        return self.state


# testing

a1 = Ad('Alfredo', datetime.datetime(2020, 5, 17, 0, 0),
        'Chinelos quase novos.', 'Venda')

print(a1.getItem())

c1 = CarAd('João', datetime.datetime(2021, 1, 5, 0, 0),
           'Dacia cor azul super estimada.', 'Venda',
           'Dacia', 'Duster 15d', 2014, 155000, 'Bom estado.')

print(c1.getAge())
c1.setState('akjdlajkd')

print(str(c1.getPublicationDate()) + ' ' + c1.getState())
