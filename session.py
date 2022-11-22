class Session:
    def __init__(self, curr_user):
        self.user = curr_user
        self.allBookings = self.loadBookings()
        self.allSpaces = self.loadSpaces()
        self.userBookings = self.getUserBookings()
    
    def loadBookings(self):
        pass

    def loadSpaces(self):
        pass

    def saveBookings(self):
        pass
    
    def saveSpaces(self):
        pass
    
    def getUserBookings(self):
        """
        Iterate through all the bookings and find the user's bookings
        """
        userBookings = []
        for booking in self.allBookings:
            if booking.userId == self.user.userId:
                userBookings.append(booking)
        return userBookings

    def viewBookings(self):
        """
        Return all bookings that the user booked
        """
        return self.userBookings
    
    def cancelBooking(self, bookingId):
        """
        Iterate through user bookings and remove the specified booking
        """
        for booking in self.userBookings:
            if booking.bookingId == bookingId:
                self.userBookings.remove(booking)
                return
    
    def addSpace(self):
        pass
    
    def removeSpace(self):
        pass