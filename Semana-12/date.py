class Date:

    def __init__(self,y,m,d,h,minutes):
        """
        __init__ Constructor for Date class

        Args:
            y (int): the year
            m (int): the month number
            d (int): the day of the month
            h (int): the hour of the day
            minutes (int): minutes

        Requires: 
            Date.isValidDate(y,m,d,h,minutes)
        """
        self.year = y
        self.month = m
        self.day = d
        self.hour = h
        self.minutes = minutes

    @staticmethod
    def isValidDate(y, m, d, h, minutes):
        pass



    def setHour(self, h):
        """
        setHour: modifies the hour of the date

        Args:
            h (int): the new value for the hour
        
        Requires: h must in range(24)

        Ensures: self.getDate() == h
        """
        self.hour = h


