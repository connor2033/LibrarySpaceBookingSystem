from models.user import User
from session import Session
from rich.console import Console
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time
from getpass import getpass
import re
import sys
import json
from datetime import date, timedelta

def main():
    global console, format
    console = Console()
    console.clear()
    format = "blink bold white"

    # title panel + login
    headerPanel = Panel("Library Space Management System", style=format)
    console.print(headerPanel)

    global session
    session = login(format)

    console.print("\nYou are now a verified user. What would you like to do?\n", style=format)

    # table with options
    table = Table(title="Select from the following options:")
    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Action", style="magenta")
    table.add_row("1","Check available spaces")
    table.add_row("2","View my bookings")
    if session.user.isLibrarian:
        table.add_row("3","Add a study space")
        table.add_row("4","Remove a study space")
    table.add_row("0","Logout")
    

    # loop for user input
    option = ""
    while not (option == "0"):
        console.print(table)
        option = input()
        if option == "0":
            console.clear()
            print("Goodbye, "+session.user.firstName)
            print("Logging out.")
            sys.exit()
        elif option == "1":
            console.clear()
            viewSpaces()
        elif option == "2":
            console.clear()
            session.viewUserBookings()
            cancelBookingPrompt()
        elif option == "3" and session.user.isLibrarian:
            console.clear()
            addSpacePrompt()
        elif option == "4" and session.user.isLibrarian:
            console.clear()
            removeSpacePrompt()

def login(format):

    console.print("\nHello! Please login.", style=format)
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    valid = False

    while valid == False:

        # Get Email
        userEmail = input("Email: ")
        if userEmail[-7:] != "@uwo.ca" or not re.fullmatch(emailRegex, userEmail):
            console.clear()
            console.print("[red]Please enter a valid UWO email address.", style=format)
            continue

        # Get password
        userPassword = getpass("Password: ")
        validCredentials, user = validateUser(userEmail, userPassword)

        if not validCredentials:
            console.clear()
            console.print("[red]Invalid Username or Password.", style=format)
            continue
        else:
            valid = True
            newSession = Session(user)

    console.clear()
    if newSession.user.isLibrarian:
        console.print("[green]Welcome, "+newSession.user.firstName+". You have librarian level permissions.", style=format)
    else:
        console.print("[green]Welcome, "+newSession.user.firstName+". You have signed in as a student.", style=format)

    return newSession

def validateUser(email, password):
    """
    Read users.json file and validate the user credentials
    """
    f = open('storage/users.json')
    data = json.load(f)

    valid = False
    user = None
    for userRecord in data:
        if userRecord['email'] == email and userRecord['password'] == password:
            valid = True
            user = User(userRecord['email'], userRecord['isLibrarian'], userRecord['firstName'], userRecord['lastName'])
            break

    f.close()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn()) as progress:

        validating = progress.add_task("[blue]Checking Credentials", total=100)
        while not progress.finished:
            progress.update(validating, advance=1)
            time.sleep(0.005)

    return valid, user

def addBookingPrompt(dayInt):
    """
    Add a new booking to the system
    """

    dates = {}
    for i in range(7):
        currDate = date.today() + timedelta(days=i)
        dates.update({i:str(currDate)})

    bookDate = dates[dayInt]
    console.print("Booking space for "+(date.today() + timedelta(days=dayInt)).strftime("%B %d, %Y"), style=format)

    # prompt to select filters
    console.print("Would you like to view a space that:",style=format)
    outlets = Prompt.ask("Has outlets", choices=["y", "n"])
    media = Prompt.ask("Has media? i.e. tv", choices=["y", "n"])
    accessible = Prompt.ask("Is accessible?", choices=["y", "n"])
    quiet = Prompt.ask("Is a quiet zone?", choices=["y", "n"])
    closed = Prompt.ask("Is a closed space?", choices=["y", "n"])
    console.print("What are the minimum number of seats that you require?", style=format)
    minSeats = input()
    pref = {
        "outlets": True if outlets == "y" else False,
        "accessible": True if accessible == "y" else False,
        "quiet": True if quiet == "y" else False,
        "private": True if closed == "y" else False,
        "media": True if media == "y" else False
    }

    # prompt to select from space availabilities
    results = False
    spaceTable = Table(title="Spaces", show_lines=True)
    spaceTable.add_column("Option", justify="right", style="cyan", no_wrap=True)
    spaceTable.add_column("Table", style="white")

    spaceIds = []
    for spaceId, space in session.allSpaces.items():
        spaceHasFilters = True
        for filterId, filterValue in space.filters.items():
            # Only keep spaces where the filter preferences match or if the preference does not matter to user
            if not (pref[filterId] == filterValue or pref[filterId] is False):
                spaceHasFilters = False
        if (spaceHasFilters) and (space.seats >= int(minSeats)):
            results = True
            spaceTable.add_row(str(spaceId), str(space.location))
            spaceIds.append(str(spaceId))

    if results:
        console.print(spaceTable)
        spaceId = Prompt.ask("What space would you like to book?:", choices=spaceIds)
    else:
        console.clear()
        console.print("There are no spaces available with your selected preferences",style=format)
        return
    
     # prompt to select time and duration of booking
    bookTime = Prompt.ask("What time would you like to book for?", choices=["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm"])
    
    # Logic to check if duration extends booking past 9pm
    durationApproved = False
    while not durationApproved:
        if (not session.user.isLibrarian):
            duration = Prompt.ask("Would you like to book this space for 1 or 2 hours?", choices=["1", "2"])
        else:
            console.print("How many hours would you like to book this space for?",style=format)
            duration = input()

        if "am" in bookTime or bookTime[:-2] == "12":
            if (int(bookTime[:-2]) + int(duration)) <= 21:
                durationApproved = True
                bookTime = int(bookTime[:-2])
            else:
                console.clear()
                console.print("[red]Invalid duration.",style=format)
        else:
            if int(bookTime[:-2]) + int(duration) <= 9:
                durationApproved = True
                bookTime = int(bookTime[:-2]) + 12
            else:
                console.clear()
                console.print("[red]Invalid duration.",style=format)


    endTime = bookDate + " " + str(int(bookTime + int(duration))) + ":00:00"
    startTime = bookDate + " " + str(bookTime) + ":00:00"

    if session.addBooking(spaceId, startTime, endTime) == False:
        console.print("This space is not available for that date and time. Please check the available spaces again.",style=format)
        return

    console.clear()
    # Confirm booking
    console.print("Your booking is confirmed for: " + startTime+"\n", style=format)

def viewSpaces():
    """
    View all available spaces
    """
    bookingsPerDay = session.getBookingsPerDay()
    tables = []

    # show weekly availabilities - display one table per day
    for day in bookingsPerDay:
        # create a table to display space availabilities
        table = Table(title="Space Availabilities for " + day.strftime("%B %d, %Y"), show_lines=True)
        table.add_column("Table", justify="right", style="cyan", no_wrap=True)

        # create 12 columns for times between 9am - 9pm (library open hours)
        for i in range(12):
            hour = i + 9
            if hour > 12:
                hour = str(hour % 12) + "pm"
            elif hour == 12:
                hour = str(12) + "pm"
            else:
                hour = str(hour) + "am"
            table.add_column(hour, style="white")

        for spaceId, space in session.allSpaces.items():
            spaceAvailability = ["" for _ in range(12)] # each empty string represents an empty space
            for booking in bookingsPerDay[day]:
                if booking.spaceId == spaceId:
                    startIndex = booking.start.hour - 9
                    endIndex = booking.end.hour - 9
                    for index in range(startIndex, endIndex):
                        spaceAvailability[index] = " [green]:heavy_check_mark:"

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

    curr = 0
    refresh = True
    viewing = True
    while viewing:

        if refresh:
            console.clear()
            console.print(tables[curr])
            refresh = False

            # Ask if user wants to book
            res = console.print("Enter (1) to book a space on this day or (2) to return to the Main Menu", style=format)
            console.print("Enter (<) to go back and (>) to go forward", style=format)
        
        res = input()

        if (res == '>' or res == '.'):
            time.sleep(0.2)
            if curr < 6:
                curr = curr+1
                refresh = True
        elif (res == '<' or res == ','):
            time.sleep(0.2)
            if curr > 0:
                curr = curr-1
                refresh = True
        elif (res == '1') or (res == 'y'):
            time.sleep(0.5)
            console.clear()
            addBookingPrompt(curr)
            return
        elif (res == '2') or (res == 'n'):
            time.sleep(0.2)
            console.clear()
            return

def removeSpacePrompt():
    """
    Displays all spaces and prompts user for space Id to delete
    """
    allSpacesTable = Table(title="All Study Spaces", show_lines=True)
    allSpacesTable.add_column("Space ID", justify="center", style="cyan", no_wrap=True)
    allSpacesTable.add_column("Location", justify="center", style="cyan", no_wrap=True)
    allSpacesTable.add_column("Number of Seats", justify="center", style="cyan", no_wrap=True)

    for spaceId, space in session.allSpaces.items():
        allSpacesTable.add_row(str(space.spaceId), space.location, str(space.seats))
    console.print(allSpacesTable)

    # Prompt to ask which space ID to remove
    console.print("What is the Space ID you would like to remove?",style=format)
    spaceId = input()

    # remove space from database
    session.removeSpace(spaceId)
    console.clear()
    console.print("Space Id " + spaceId + " has been removed from the System\n",style=format)

def addSpacePrompt():
    """
    Prompt user for space details, then call function to add the space
    """
    console.print("Adding a Study Space, Please answer the following:",style=format)

    # Prompt to input filters
    console.print("Please enter the location name (ex. Taylor - Room 155)",style=format)
    spaceName = input()
    outlets = Prompt.ask("Has outlets", choices=["y", "n"])
    media = Prompt.ask("Has media? i.e. tv", choices=["y", "n"])
    accessible = Prompt.ask("Is accessible?", choices=["y", "n"])
    quiet = Prompt.ask("Is a quiet zone?", choices=["y", "n"])
    closed = Prompt.ask("Is a closed space?", choices=["y", "n"])
    console.print("What are the minimum number of seats available?",style=format)
    minSeats = input()

    # add space to database
    session.addSpace(spaceName, 
                    minSeats, 
                    "True" if outlets == "y" else "False", 
                    "True" if media == "y" else "False", 
                    "True" if accessible == "y" else "False", 
                    "True" if quiet == "y" else "False", 
                    "True" if closed == "y" else "False"
                    )
    console.clear()
    console.print(spaceName + " has been added to the system", style=format)

def cancelBookingPrompt():
    """
    Ask user if they would like to cancel a booking
    """
    console.print("What would you like to do? Enter (1) to cancel a booking or (2) to return to the Main Menu", style=format)
    action = int(input())

    # return to main menu if input == 1
    if action == 2:
        console.clear()
        return

    console.print("Please enter the booking id you would like to cancel: ", style=format)
    bookingId = int(input())

    if session.cancelBooking(bookingId) is False:
        console.print("Invalid booking ID", style=format)
        cancelBookingPrompt()
    else:
        console.clear()
        console.print("Booking " + str(bookingId) + " successfully cancelled.\n",style=format)


if __name__ == '__main__':
    main()
