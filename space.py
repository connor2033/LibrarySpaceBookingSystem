class Space:
    
    spaceId = 0
    seats = 0
    filters = {}
    location = ""

    def __init__(self, spaceId, seats, filters, location):
        self.spaceId = spaceId
        self.seats = seats
        self.filters = filters
        self.location = location
   