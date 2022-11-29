class Space:

    def __init__(self, spaceId, seats, filters, location):
        self.spaceId = spaceId
        self.seats = seats
        self.filters = filters
        self.location = location
    
    def toDict(self):
        return {
            "spaceId": self.spaceId,
            "location": self.location,
            "seats": self.seats,
            "filters": self.filters
        }