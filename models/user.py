class User:
   

    def __init__(self, userId, isLibrarian, firstName, lastName):
        self.userId = userId
        self.isLibrarian = isLibrarian
        self.firstName = firstName
        self.lastName = lastName
        self.bookings = []
   