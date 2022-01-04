class Player:
    def __init__(self, pName, pBal):
        self.name = pName
        self.balance = pBal
        self.discounts = {}
        self.rentSplits = {}
        self.bankrupt = False

    def addFunds(self, amt: int):
        self.balance += amt

    def takeFunds(self, amt: int):
        self.balance -= amt
        if self.balance < 0:
            self.goBankrupt()

    def addDiscount(self, percentage: int, location: str):
        if location in self.discounts.keys():
            self.discounts[location] += percentage
        else:
            self.discounts[location] = percentage

    def addRentSplit(self, percentage: int, location: str):
        if location in self.rentSplits.keys():
            self.rentSplits[location] += percentage
        else:
            self.rentSplits[location] = percentage

    def checkRebate(self, list, val):
        if val in list.keys():
            return list[val]
        else:
            return 0

    def isBankrupt(self) -> bool:
        if self.bankrupt:
            return True
        else:
            return False

    def goBankrupt(self) -> None:
        self.bankrupt = True