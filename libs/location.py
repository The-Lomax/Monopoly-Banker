class Location:
    def __init__(self, lName):
        self.name = lName
        self.discounts = {}
        self.rentSplits = {}

    def addDiscount(self, player, percentage):
        if player in self.discounts.keys():
            self.discounts[player] += percentage
        else:
            self.discounts[player] = percentage
        if self.discounts[player] > 100:
            self.discounts[player] = 100

    def addRentSplit(self, player, percentage):
        if player in self.rentSplits.keys():
            self.rentSplits[player] += percentage
        else:
            self.rentSplits[player] = percentage
