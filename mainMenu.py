from booking import Booking
from space import Space
from user import User
from session import Session

import datetime

def main():
    print("Hello world!")
    addSpace()
    bookSpace()
    print("Booking "+str(bookings[0].bookingId)+" is in space "+str(bookings[0].spaceId)+" and is held by "+bookings[0].userId)

def login():
    user = User("chaines4@uwo.ca", isLibrarian=False)
    return

def logout():
    return

if __name__ == '__main__':
    main()