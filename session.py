import json
from datetime import datetime
from datetime import date
from datetime import timedelta
from rich.table import Table
from rich.console import Console
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
                spaceId = space['spaceId'],
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
                spaceId = self.allSpaces[nextSpace],
                seats = self.allSpaces[seats],
                filters = self.allSpaces[filters],
                location = self.allSpaces[location]
            )

        self.allSpaces[nextSpace] = newSpace


    def removeSpace(self, spaceId):
        del self.allSpaces[spaceId]

    def viewSpace(self):
        # set up properties and console for rich library and pretty layout
        console = Console()
        format = "blink bold white"

        # retrieve all the bookings corresponding to the next 7 days
        bookingsPerDay = {}
        currDate = date.today()
        for i in range(7):
            currDate = currDate + timedelta(days=i)
            bookingsPerDay[currDate] = [] # create an empty list to store the list of bookings for the day

        for booking in self.allBookings.values():
            bookingsPerDay[booking.start.date()].append(booking)

        # show weekly availabilities - display one table per day
        for day in bookingsPerDay:
            table = Table(title="Space Availabilities for " + day.strftime("%B %d, %Y"), show_lines=True) # create a table to display space availabilities
            table.add_column("Table", justify="right", style="cyan", no_wrap=True)

            # create 12 columns for times between 9am - 9pm (library open hours)
            for i in range(13):
                time = i + 9
                if time > 12:
                    time = str(time % 12) + "pm"
                else:
                    time = str(time) + "am"
                table.add_column(time, style="white")

            # spaces = self.allSpaces
            for spaceId, space in self.allSpaces.items():
                spaceAvailability = ["" for _ in range(12)] # each empty string represents an empty space
                for booking in bookingsPerDay[day]:
                    if booking.spaceId == spaceId:
                        startIndex = booking.start.hour - 9
                        endIndex = booking.end.hour - 9
                        for index in range(startIndex, endIndex):
                            spaceAvailability[index] = "[green]:heavy_check_mark:"

                table.add_row(
                    space.location,
                    spaceAvailability[0],
                    spaceAvailability[1],
                    spaceAvailability[2],
                    spaceAvailability[3],
                    spaceAvailability[4],
                    spaceAvailability[5],
                    spaceAvailability[6],
                    spaceAvailability[7],
                    spaceAvailability[8],
                    spaceAvailability[9],
                    spaceAvailability[10],
                    spaceAvailability[11]
                )

            console.print(table)

        # Ask if user wants to book
        console.print("Would you like to book a space? Please enter Y for yes or N for no", style=format)

