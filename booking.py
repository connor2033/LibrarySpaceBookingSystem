import datetime

class Booking:
   

    def __init__(self, bookingId, spaceId, userId, start, end):
        self.bookingId = bookingId
        self.spaceId = spaceId
        self.userId = userId
        self.start = start
        self.end = end
   