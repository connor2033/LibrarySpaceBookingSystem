import datetime

class Booking:
   
    def __init__(self, bookingId, spaceId, userId, start, end):
        self.bookingId = bookingId
        self.spaceId = spaceId
        self.userId = userId
        self.start = start
        self.end = end

    def toDict(self):
        return {
            "bookingId": self.bookingId,
            "spaceId": self.spaceId,
            "userEmail": self.userId,
            "startTime": str(self.start),
            "endTime": str(self.end)
        }