import datetime
from booking import Booking
from space import Space
from user import User
from session import Session
from rich.console import Console
from rich import print
from rich.panel import Panel
from rich.table import Table
import sys

def main():
    # title panel + login
    console = Console()
    format = "blink bold white"
    print(Panel("Library Space Management System", style=format))
    console.print("\nHello! Please login.", style=format)
    console.print(
        "You are now a verified user. What would you like to do?\n", style=format)

    # table with options
    table = Table(title="Select from the following options:")
    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Action", style="magenta")
    table.add_row("1","Check available spaces")
    table.add_row("2","View my bookings")
    table.add_row("3","Add a study space")
    table.add_row("4","Remove a study space")
    table.add_row("0","Logout")
    console.print(table)

    # loop for user input
    option = ""
    while not (option == "0"):
        option = input()
        if option == "0":
            sys.exit()
        elif option == "1":
            print("View bookings")
        elif option == "2":
            print("View bookings")
        elif option == "3":
            print("View bookings")
        elif option == "4":
            print("View bookings")

    # addSpace()
    # bookSpace()
    # print("Booking "+str(bookings[0].bookingId)+" is in space "+str(bookings[0].spaceId)+" and is held by "+bookings[0].userId)

# def login():
#     user = User("chaines4@uwo.ca", isLibrarian=False)
#     return


# def logout():
#     return


# def bookSpace():
#     # datetime(year, month, day, hour, minute, second, microsecond)
#     startTime = datetime.datetime(2022, 11, 15, 14)
#     endTime = datetime.datetime(2022, 11, 15, 16)
#     newBooking = Booking(22, spaces[0].spaceId,
#                          "chaines4@uwo.ca", startTime, endTime)
#     bookings.append(newBooking)
#     print("Booking added")

#     return

# def addSpace():
#     newSpace = Space(123, 4, "filters", "Taylor Library 155")
#     spaces.append(newSpace)
#     print("Space added")
#     return


if __name__ == '__main__':
    main()
