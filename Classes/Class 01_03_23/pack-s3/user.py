class User:
    """
    Author: Thibault Langlois

     This class represents a User. Each user is defined by its 
     name and its email address.
    """

    def __init__(self, name, email):
        """
        __init__ The constructor

        Args:
            name (string): User's name
            email (string): User's email address
        """
        self.name = name
        self.email = email

    def getName(self):
        """
        getName: Returns the user's name.

        Returns:
            string: the user's name.
        """
        return self.name

    def getEmail(self):
        """
        getEmail: Returns user's email address.

        Returns:
            string: the user's email address
        """
        return self.email

    def setName(self, newname):
        """
        setName: change user's name.

        Args:
            newname (string): the new name 
        """
        self.name = newname

    def setEmail(self, newemail):
        """
        setEmail: change user's email address.

        Args:
            newemail (string): the new email address.
        """
        self.email = newemail


 