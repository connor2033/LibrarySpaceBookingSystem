class Session:
    def __init__(self, curr_user):
        self.user = curr_user
        self.allBookings = self.loadBookings()
        self.allSpaces = self.loadSpaces()
    
    def loadBookings(self):
        pass

    def loadSpaces(self):
        pass

    def saveBookings(self):
        pass
    
    def saveSpaces(self):
        pass
    
    def viewBookings(self):
        
        pass
    
    def cancelBooking(self):
        pass
    
    def addSpace(self):
        pass
    
    def removeSpace(self):
        pass