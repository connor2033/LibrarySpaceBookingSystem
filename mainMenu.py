import datetime
from booking import Booking
from space import Space
from user import User
from session import Session
from rich.console import Console
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time
from getpass import getpass
import re
import sys
import json

console = Console()
session = None

def main():
    # title panel + login
    format = "blink bold white"
    print(Panel("Library Space Management System", style=format))

    # create a global session object for the current user
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
    console.print(table)

    # loop for user input
    option = ""
    while not (option == "0"):
        option = input()

        # logout
        if option == "0":
            console.clear()
            print("Goodbye, "+session.user.firstName)
            print("Logging out.")
            sys.exit()

        # view all spaces for the next 7 days
        elif option == "1":
            console.clear()
            session.viewSpace()

        # view all the user's bookings
        elif option == "2":
            console.clear()
            print("View my bookings")
            session.viewUserBookings()
            session.cancelBookingPrompt()
        
        # allow librarians to add study spaces
        elif option == "3" and session.user.isLibrarian:
            console.clear()
            print("Add a study space")

        # allow librarians to delete study spaces
        elif option == "4" and session.user.isLibrarian:
            console.clear()
            print("Remove a study space")
        console.print(table)

def login(format):
    """
    Prompt user for login credentials to start a new session
    """
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
        
        # Prompt user again for credentials if invalid
        if not validCredentials:
            console.clear()
            console.print("[red]Invalid Username or Password.", style=format)
            continue
        
        # otherwise, create a new session 
        else:
            valid = True
            newSession = Session(user)

    # Greeting message
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


if __name__ == '__main__':
    main()
