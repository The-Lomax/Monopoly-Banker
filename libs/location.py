class Location:
    def __init__(self, lName):
        self.name = lName
        self.discounts = {}
        self.rentSplits = {}

    def addDiscount(self, player, percentage):
        self.discounts[player] = percentage

    def addRentSplit(self, player, percentage):
        self.rentSplits[player] = percentage
