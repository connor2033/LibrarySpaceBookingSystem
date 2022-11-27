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

    global session
    session = login(format)
    if session.user.isLibrarian:
        console.print("Welcome, "+session.user.firstName+". You have librarian level permissions.", style=format)
    else:
        console.print("Welcome, "+session.user.firstName+". You have signed in as a student.", style=format)

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
        if option == "0":
            console.clear()
            print("Goodbye, "+session.user.firstName)
            print("Logging out.")
            sys.exit()
        elif option == "1":
            console.clear()
            print("Check available spaces")
        elif option == "2":
            console.clear()
            print("View my bookings")
            # Option to cancel booking here
        elif option == "3" and session.user.isLibrarian:
            console.clear()
            print("Add a study space")
        elif option == "4" and session.user.isLibrarian:
            console.clear()
            print("Remove a study space")

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

        task1 = progress.add_task("[blue]Checking Credentials", total=100)

        while not progress.finished:
            progress.update(task1, advance=1)
            time.sleep(0.005)
    
    return valid, user


if __name__ == '__main__':
    main()
