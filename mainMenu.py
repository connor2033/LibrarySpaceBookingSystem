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
import json

console = Console()
session = None

def main():
    # title panel + login

    format = "blink bold white"
    print(Panel("Library Space Management System", style=format))

    global session
    session = login(format)
    console.print("Welcome "+session.user.userId, style=format)

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
            session.viewSpace()
        elif option == "2":
            print("View my bookings")
        elif option == "3":
            print("Add a study space")
        elif option == "4":
            print("Remove a study space")

def login(format):

    console.print("\nHello! Please login.", style=format)
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    valid = False

    while valid == False:

        # Get Email
        userEmail = input("Email: ")
        if userEmail[-7:] != "@uwo.ca" or not re.fullmatch(emailRegex, userEmail):
            console.print("Please enter a valid UWO email address.", style=format)
            continue

        # Get password
        userPassword = getpass("Password: ")
        validCredentials, user = validateUser(userEmail, userPassword)

        if not validCredentials:
            console.print("Invalid Username or Password.", style=format)
            continue
        else:
            valid = True
            newSession = Session(user)

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
            user = User(userRecord['email'], userRecord['isLibrarian'])
            break

    f.close()
    return valid, user


if __name__ == '__main__':
    main()
