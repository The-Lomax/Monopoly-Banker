class Location:
    def __init__(self, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId):
        self.id = lId
        self.name = name
        self.buyPrice = buyPrice
        self.rent = rent
        self.mortgage = mortgage
        self.buildPrice = buildPrice
        self.buildings = buildings
        self.discounts = rentDiscounts
        self.rentSplits = rentSplits
        self.status = status
        self.ownerId = ownerId

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
