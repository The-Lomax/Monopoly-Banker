class POI:
    def __init__(self, lType, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.type = lType
        self.id = lId
        self.name = name
        self.buyPrice = buyPrice
        self.rent = rent
        self.mortgage = mortgage
        self.status = status
        self.ownerId = ownerId

    def locateOwner(self, players):
        for el in players.values():
            if el.id == self.ownerId:
                return el