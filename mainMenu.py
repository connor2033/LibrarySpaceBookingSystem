import datetime
from booking import Booking
from space import Space
from user import User
from session import Session
from rich.console import Console
from rich import print
from rich.panel import Panel
from rich.table import Table
from getpass import getpass
import re
import sys

console = Console()

def main():
    # title panel + login
    
    format = "blink bold white"
    print(Panel("Library Space Management System", style=format))

    login(format)
    # console.print("\nHello! Please login.", style=format)
    # userEmail = input("Email: ")
    # userPassword = getpass("Password: ")

    console.print("\nYou are now a verified user. What would you like to do?\n", style=format)

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
            print("Logout ")
            sys.exit()
        elif option == "1":
            print("Check available spaces")
        elif option == "2":
            print("View my bookings")
        elif option == "3":
            print("Add a study space")
        elif option == "4":
            print("Remove a study space")

def login(format):
    console.print("\nHello! Please login.", style=format)

    emailHost = ""
    regexMatch = False
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    while emailHost != "@uwo.ca" or regexMatch == False:
        userEmail = input("Email: ")
        emailHost = userEmail[-7:]
        regexMatch = re.fullmatch(emailRegex, userEmail)
        if emailHost != "@uwo.ca" or regexMatch == False:
            console.print("Please enter a valid UWO email address.", style=format)


    userPassword = getpass("Password: ")

    # user = User("chaines4@uwo.ca", isLibrarian=False)
    return

if __name__ == '__main__':
    main()
