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
        """
        Read bookings.json file and loads the data into a dictionary (key, value) = (id, Booking obj)
        """
        f = open('storage/bookings.json')
        data = json.load(f)

        bookings = {}
        for booking in data:
            newBooking = Booking(
                bookingId = booking['bookingId'],
                spaceId = booking['spaceId'],
                userId = booking['userEmail'],
                start = datetime.strptime(booking['startTime'], '%Y-%m-%d %H:%M'),
                end = datetime.strptime(booking['endTime'], '%Y-%m-%d %H:%M')
            )
            bookings[booking['bookingId']] = newBooking
        
        f.close()
        return bookings

    def loadSpaces(self):
        """
        Read spaces.json file and loads the data into a dictionary (key, value) = (id, Space obj)
        """
        f = open('storage/spaces.json')
        data = json.load(f)

        spaces = {}
        for space in data:
            newSpace = Space(
                spacesId = space['spaceId'],
                seats = space['seats'],
                filters = space['filters'],
                location = space['location']
            )
            spaces[space['spaceId']] = newSpace

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
        for booking in self.allBookings.values():
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
        for booking in self.userBookings.values():
            if booking.bookingId == bookingId:
                self.userBookings.remove(booking)
                return
    
    def addSpace(self, spaceId, location, seats, outlets, accessible, quiet, private, media):
        
        nextSpace = max(self.allSpaces.keys()) + 1

        filters = {
            "outlets": outlets,
            "accesible": accessible,
            "quiet": quiet,
            "private":private,
            "media":media

        }
        newSpace = Space(
                spacesId = self.allSpaces[nextSpace],
                seats = self.allSpaces[seats],
                filters = self.allSpaces[filters],
                location = self.allSpaces[location]
            )
        
        self.allSpaces[nextSpace] = newSpace
        
    
    def removeSpace(self, spaceId):
        del self.allSpaces[spaceId]