import json
from datetime import datetime

from booking import Booking
from space import Space
from user import User

class Session:
    def __init__(self, curr_user):
        self.user = curr_user
        self.allBookings = self.loadBookings()
        self.allSpaces = self.loadSpaces()
        self.userBookings = self.getUserBookings()
    
    def loadBookings(self):
        f = open('storage/bookings.json')
        data = json.load(f)

        bookings = []
        for booking in data:
            newBooking = Booking(
                bookingId = booking['bookingId'],
                spaceId = booking['spaceId'],
                userId = booking['userEmail'],
                start = datetime.strptime(booking['startTime'], '%Y-%m-%d %H:%M'),
                end = datetime.strptime(booking['endTime'], '%Y-%m-%d %H:%M')
            )
            bookings.append(newBooking)
        
        f.close()
        return bookings

    def loadSpaces(self):
        f = open('storage/spaces.json')
        data = json.load(f)

        spaces = []
        for space in data:
            newSpace = Space(
                spacesId = space['spaceId'],
                seats = space['seats'],
                filters = space['filters'],
                location = space['location']
            )
            spaces.append(newSpace)
        f.close()
        return spaces

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