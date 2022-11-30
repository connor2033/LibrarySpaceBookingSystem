from datetime import date
from datetime import timedelta
import json
from rich.table import Table
from rich.console import Console
from models.booking import Booking
from models.space import Space
from datetime import datetime

class Session:

    def __init__(self, curr_user):
        self.spaces_filename = 'storage/spaces.json'
        self.bookings_filename = 'storage/bookings.json'
        self.user = curr_user
        self.allBookings = self.loadBookings()
        self.allSpaces = self.loadSpaces()

    def loadBookings(self):
        """
        Read bookings.json file and loads the data into a dictionary (key, value) = (id, Booking obj)
        """
        f = open(self.bookings_filename)
        data = json.load(f)

        bookings = {}
        for booking in data:
            # we don't want to load bookings that are past
            bookingEndTime = datetime.strptime(booking['endTime'], '%Y-%m-%d %H:%M:%S')
            if bookingEndTime < datetime.now():
                continue
            # if the booking is in the future, append to our list
            newBooking = Booking(
                bookingId = booking['bookingId'],
                spaceId = booking['spaceId'],
                userId = booking['userEmail'],
                start = datetime.strptime(booking['startTime'], '%Y-%m-%d %H:%M:%S'),
                end = datetime.strptime(booking['endTime'], '%Y-%m-%d %H:%M:%S')
            )
            bookings[booking['bookingId']] = newBooking

        f.close()

        # update bookings in the database to include only future bookings
        json_object = json.dumps(self.getJson(bookings), indent=4)
        with open(self.bookings_filename, "w") as f:
            f.write(json_object)

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

    def getBookingsPerSpace(self, spaceId):
        """
        Helper function to retrieve all the bookings for a certain space
        """
        bookings = []
        for booking in self.allBookings.values():
            if booking.spaceId == int(spaceId):
                bookings.append(booking)
        return bookings

    def getBookingsPerDay(self):
        """
        Retrieve all the bookings corresponding to the next 7 days
        """
        bookingsPerDay = {}
        currDate = date.today()
        for i in range(7):
            currDate = date.today() + timedelta(days=i)
            bookingsPerDay[currDate] = [] # create an empty list to store the list of bookings for the day

        # add all bookings for that day into a list
        for booking in self.allBookings.values():
            if booking.start.date() in bookingsPerDay:
                bookingsPerDay[booking.start.date()].append(booking)

        return bookingsPerDay

    def addBooking(self, spaceId, startTime, endTime):
        """
        Checks if booking time does not overlap with an existing booking, then adds it to the database
        """
        # verify that chosen time is in the future
        if  datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S') < datetime.now():
            return False

        # verify that there isn't already a booking with the specified start time
        for booking in self.getBookingsPerSpace(spaceId):
            # case 1: an existing booking is nested inside the chosen time
            if booking.start >= datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S') and booking.end <= datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S'):
                print(booking.start, booking.end)
                return False
            # case 2: start time is nested inside an existing booking time
            if datetime.strptime(startTime,'%Y-%m-%d %H:%M:%S') >= booking.start and datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S') <= booking.end:
                print("case 2")
                return False
            # case 3: end time is nested inside an existing booking time
            if datetime.strptime(endTime,'%Y-%m-%d %H:%M:%S') >= booking.start and datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S') >= booking.end:
                print("case 3")
                return False

        # Get the next booking id
        nextBookingId = 1
        if self.allBookings:
            nextBookingId = max(self.allBookings.keys()) + 1


        # Create a new booking
        newBooking = Booking(nextBookingId, int(spaceId), self.user.userId, datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S'), datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S'))

        # Add booking to the system and database
        self.allBookings[nextBookingId] = newBooking

        json_object = json.dumps(self.getJson(self.allBookings), indent=4)
        with open(self.bookings_filename, "w") as f:
            f.write(json_object)

        return newBooking


    def cancelBooking(self, bookingId, cancelForAllUsers=False):
        """
        Iterate through user bookings and remove the specified booking
        """
        bookingExists = False
        for booking in self.getUserBookings():
            if bookingId == booking.bookingId:
                bookingExists = True

        if bookingExists or cancelForAllUsers:
            # Delete the booking from the all bookings dictionary
            del self.allBookings[bookingId]

            # Update the database
            json_object = json.dumps(self.getJson(self.allBookings), indent=4)
            with open(self.bookings_filename, "w") as f:
                f.write(json_object)

            # return true if booking was cancelled
            return True

        # return false if booking not found in user bookings
        else:
            return False

    def addSpace(self, spaceName, minSeats, outlets="False", media="False", accessible="False", quiet="False", closed="False"):
        # Finding new unique key to add to the space json file
        nextSpace = max(self.allSpaces.keys()) + 1

        # Build filters dictionary
        filters = {
            "outlets": eval(outlets),
            "accessible": eval(accessible),
            "quiet": eval(quiet),
            "private": eval(closed),
            "media": eval(media)
        }

        # Create new space
        newSpace = Space(
            spaceId = nextSpace,
            seats = int(minSeats),
            location = spaceName,
            filters = filters,
        )

        # Add space to System
        self.allSpaces[nextSpace] = newSpace

        # Update the database
        json_object = json.dumps(self.getJson(self.allSpaces), indent=4)
        with open(self.spaces_filename, "w") as f:
            f.write(json_object)

        return newSpace

    def removeSpace(self, spaceId):
        """
        Removes space from database
        """
        # Delete space from system
        del self.allSpaces[int(spaceId)]

        tempSpaces = self.allBookings.copy()
        for bookingId, booking in tempSpaces.items():
            if booking.spaceId == int(spaceId):
                self.cancelBooking(bookingId, cancelForAllUsers=True)

        # Remove from the database
        json_object = json.dumps(self.getJson(self.allSpaces), indent=4)
        with open(self.spaces_filename, "w") as f:
            f.write(json_object)

    def getJson(self, dictionary):
        """
        Converts a dictionary of objects (bookings or spaces) to a json parsable format.
        """
        json = []
        for value in dictionary.values():
            json.append(value.toDict())
        return json

    def viewUserBookings(self):
        """
        Displays all bookings for the current user and asks if they want to cancel a booking
        """
        # set up properties and console for rich library and pretty layout
        console = Console()
        format = "blink bold white"

        # create a table to display all user bookings
        table = Table(title="Bookings for " + self.user.firstName + " " + self.user.lastName, show_lines=True)
        table.add_column("Booking ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Location", justify="right", style="cyan", no_wrap=True)
        table.add_column("Start Time", justify="right", style="cyan", no_wrap=True)
        table.add_column("End Time", justify="right", style="cyan", no_wrap=True)

        # for each booking, create a new row for the booking in the table
        userBookings = self.getUserBookings()
        for booking in userBookings:
            location = self.allSpaces[booking.spaceId].location
            table.add_row(str(booking.bookingId), location, str(booking.start), str(booking.end))

        # clear console and display the table
        console.clear()
        console.print(table)