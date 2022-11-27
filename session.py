import json
from datetime import datetime

from booking import Booking
from space import Space
from user import User

class Session:
    def __init__(self, curr_user):
        self.spaces_filename = 'storage/spaces.json'
        self.bookings_filename = 'storage/bookings.json'
        self.user = curr_user
        self.allBookings = self.loadBookings()
        self.allSpaces = self.loadSpaces()
        self.userBookings = self.getUserBookings()
    
    def loadBookings(self):
        """
        Read bookings.json file and loads the data into a dictionary (key, value) = (id, Booking obj)
        """
        f = open(self.bookings_filename)
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
        f = open(self.spaces_filename)
        data = json.load(f)

        spaces = {}
        for space in data:
            newSpace = Space(
                spaceId = space['spaceId'],
                seats = space['seats'],
                filters = space['filters'],
                location = space['location']
            )
            spaces[space['spaceId']] = newSpace

        f.close()
        return spaces
    
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
                # Remove the booking from memory
                del self.userBookings[bookingId]
                del self.allBookings[bookingId]

                # Update the database
                json_object = json.dumps(self.getJson(self.allBookings), indent=4)
                with open(bookings_filename, "w") as f:
                    f.write(json_object)
                return  
    
    def addSpace(self, location, seats, outlets=False, accessible=False, quiet=False, private=False, media=False):
        # Get the next space ID
        nextSpace = max(self.allSpaces.keys()) + 1

        # Build filters dictionary
        filters = {
            "outlets": outlets,
            "accesible": accessible,
            "quiet": quiet,
            "private":private,
            "media":media

        }

        # Create new space
        newSpace = Space(
            spaceId = nextSpace,
            seats = seats,
            filters = filters,
            location = location
        )
        
        self.allSpaces[nextSpace] = newSpace

        # Update the database
        json_object = json.dumps(self.getJson(self.allSpaces), indent=4)
        with open(self.spaces_filename, "w") as f:
            f.write(json_object)
        
        return newSpace
    
    def removeSpace(self, spaceId):
        del self.allSpaces[spaceId]

    def getJson(self, dictionary):
        json = []
        for value in dictionary.values():
            json.append(value.toDict())
        return json