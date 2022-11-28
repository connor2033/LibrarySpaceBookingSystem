from datetime import date
from datetime import timedelta
import datetime
import json
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from booking import Booking
from space import Space
from user import User
from datetime import datetime
import sys
import keyboard
import time

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
                start = datetime.strptime(booking['startTime'], '%Y-%m-%d %H:%M:%S'),
                end = datetime.strptime(booking['endTime'], '%Y-%m-%d %H:%M:%S')
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

    def addBooking(self):
        """
        Add a new booking to the system
        """
        # set up properties and console for rich library and pretty layout
        console = Console()
        format = "blink bold white"

        # table with day options
        table = Table(title="Days Available")
        table.add_column("Option", justify="right", style="cyan", no_wrap=True)
        table.add_column("Action", style="magenta")
        option = ""
        dates = {}
        for i in range(7):
            currDate = date.today() + timedelta(days=i)
            dates.update({str(i):str(currDate)})
            table.add_row(str(i),currDate.strftime("%B %d, %Y"))

        # request date of booking
        console.print("What day would you like to book for? Please enter the option:", style=format)
        console.print(table)
        option = input()
        bookDate = dates[option]

        # prompt to select filters
        console.print("Would you like to view a space that:")
        outlets = Prompt.ask("Has outlets", choices=["True", "False"])
        media = Prompt.ask("Has media? i.e. tv", choices=["True", "False"])
        accessible = Prompt.ask("Is accessible?", choices=["True", "False"])
        quiet = Prompt.ask("Is a quiet zone?", choices=["True", "False"])
        closed = Prompt.ask("Is a closed space?", choices=["True", "False"])
        console.print("What are the minimum number of seats that you require?", style=format)
        minSeats = input()
        pref = {
            "outlets": eval(outlets),
            "accessible": eval(accessible),
            "quiet": eval(quiet),
            "private": eval(closed),
            "media": eval(media)
        }

        # prompt to select from space availabilities
        results = False
        spaceTable = Table(title="Spaces", show_lines=True)
        spaceTable.add_column("Option", justify="right", style="cyan", no_wrap=True)
        spaceTable.add_column("Table", style="white")
        for spaceId, space in self.allSpaces.items():
            # console.print(pref)
            # console.print(space.filters)
            if (space.filters == pref) and (space.seats >= int(minSeats)):
                results = True
                spaceTable.add_row(str(spaceId), str(space.location))
        if results:
            console.print("What space would you like to book?:", style=format)
            console.print(spaceTable)
            spaceId = input()
        else:
            console.print("There are no spaces booked on your selected preferences")
            # Time delay
            # console.clear()
            return

        # prompt to select time and duration of booking
        bookTime = Prompt.ask("What time would you like to book for?", choices=["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"])
        if (not self.user.isLibrarian):
            duration = Prompt.ask("Would you like to book this space for 1 or 2 hours?", choices=["1", "2"])
        else:
            console.print("How many hours would you like to book this space for?")
            duration = input()

        # convert booking time to a datetime formatted string
        if "am" in bookTime:
            bookTime = int(bookTime.strip("am"))
        else:
            bookTime = int(bookTime.strip("pm"))
            
        endTime = bookDate + " " + str(int(bookTime + int(duration))) + ":00:00"
        bookDate = bookDate + " " + str(bookTime) + ":00:00"

        # Get the next booking id
        nextBookingId = max(self.allBookings.keys()) + 1

        # Create a new booking
        newBooking = Booking(nextBookingId, int(spaceId), self.user.userId, bookDate, endTime)

        # Add booking to the system and database
        self.allBookings[nextBookingId] = newBooking

        json_object = json.dumps(self.getJson(self.allBookings), indent=4)
        with open(self.bookings_filename, "w") as f:
            f.write(json_object)

        # Confirm booking
        console.print("Your booking is confirmed for: " + bookDate, style=format)

        return newBooking



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
                with open(self.bookings_filename, "w") as f:
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

        # Update the database
        json_object = json.dumps(self.getJson(self.allSpaces), indent=4)
        with open(self.spaces_filename, "w") as f:
            f.write(json_object)
        

    def getJson(self, dictionary):
        json = []
        for value in dictionary.values():
            json.append(value.toDict())
        return json


    def viewSpace(self):
        # set up properties and console for rich library and pretty layout
        console = Console()
        format = "blink bold white"

        # TODO: can move this into a separate function
        # retrieve all the bookings corresponding to the next 7 days
        bookingsPerDay = {}
        currDate = date.today()
        for i in range(7):
            currDate = date.today() + timedelta(days=i)
            bookingsPerDay[currDate] = [] # create an empty list to store the list of bookings for the day
        # add all bookings for that day into a list
        for booking in self.allBookings.values():
            if booking.start.date() in bookingsPerDay:
                bookingsPerDay[booking.start.date()].append(booking)

        tables = []

        # show weekly availabilities - display one table per day
        for day in bookingsPerDay:
            # create a table to display space availabilities
            table = Table(title="Space Availabilities for " + day.strftime("%B %d, %Y"), show_lines=True)
            table.add_column("Table", justify="right", style="cyan", no_wrap=True)

            # create 12 columns for times between 9am - 9pm (library open hours)
            for i in range(13):
                hour = i + 9
                if hour > 12:
                    hour = str(hour % 12) + "pm"
                else:
                    hour = str(hour) + "am"
                table.add_column(hour, style="white")

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

            tables.append(table)
            # console.print(table)

        curr = 0
        refresh = True
        viewing = True
        while viewing:
            
            if refresh:
                console.clear()
                console.print(tables[curr])
                refresh = False

                console.print("Press < > to cycle through tables", style=format)
                # Ask if user wants to book
                console.print("Would you like to book a space? Please enter Y for yes or N for no", style=format)

            if keyboard.is_pressed('right'):
                time.sleep(0.2)
                if curr < 6:
                    curr = curr+1
                    refresh = True
            elif keyboard.is_pressed('left'):
                time.sleep(0.2)
                if curr > 0:
                    curr = curr-1
                    refresh = True
            elif keyboard.is_pressed('Y') or keyboard.is_pressed('y'):
                time.sleep(0.5)
                console.clear()
                self.addBooking()
                return
            elif keyboard.is_pressed('N') or keyboard.is_pressed('n'):
                time.sleep(0.2)
                return


