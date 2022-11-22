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

def bookSpace():
    # datetime(year, month, day, hour, minute, second, microsecond)
    startTime = datetime.datetime(2022, 11, 15, 14)
    endTime = datetime.datetime(2022, 11, 15, 16)
    newBooking = Booking(22, spaces[0].spaceId, "chaines4@uwo.ca", startTime, endTime)
    bookings.append(newBooking)
    print("Booking added")

    return

# def addSpace():
#     newSpace = Space(123, 4, "filters", "Taylor Library 155")
#     spaces.append(newSpace)
#     print("Space added")
#     return

if __name__ == '__main__':
    main()