from tkinter import messagebox


class Location:
    def __init__(self, lType, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId):
        self.type = lType
        self.id = lId
        self.name = name
        self.buyPrice = buyPrice
        self.rent = rent
        self.mortgage = mortgage
        self.buildPrice = buildPrice
        self.buildings = buildings
        self.discounts = rentDiscounts
        self.rentSplits = rentSplits
        self.status = status  # possible states: "free" if unowned, "active" if owned but not mortgaged, "mortgaged" if mortgaged
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
    
    def setOwnership(self, player):
        self.ownerId = player.id
    
    def build(self, players, amt):
        # check building lots available
        if self.buildings + amt > 5: return messagebox.showerror("error", f"Can build max {5 - self.buildings}.")

        # check if location is permitted to build
        if not self.status == "active": return messagebox.showerror("error", "No building permission.")

        # check if owner has sufficient funds
        owner = self.locateOwner(players)
        bill = amt * self.buildPrice
        if not owner.balance >= bill: return messagebox.showerror("error", "Insufficient funds.")
        
        # assume that by now there are lots available, location is permitted to build, and owner is found and has funds
        owner.adjustBalance(-bill)
        self.buildings += amt
    
    def bulldoze(self, players, amt):
        # check if sufficient buildings to destroy
        if self.buildings < amt: return messagebox.showerror("error", f"Can bulldoze max {self.buildings}.")

        # get owner and write up the bill
        owner = self.locateOwner(players)
        bill = amt * self.buildPrice
        
        # bulldoze the lot and pay the owner
        owner.adjustBalance(bill)
        self.buildings -= amt
    
    def locateOwner(self, players):
        for el in players.values():
            if el.id == self.ownerId:
                return el
    
    def toggleMortgage(self, players):
        owner = self.locateOwner(players)

        # check if location is mortgaged or not
        if self.status == "active": self.buyMortgage(owner)
        elif self.status == "mortgaged": self.payMortgage(owner)
    
    def buyMortgage(self, owner):
        # check if there are buildings in the property
        if self.buildings > 0: return messagebox.showerror("error", "Sell buildings first.")

        self.status = "mortgaged"
        owner.adjustBalance(self.mortgage)
    
    def payMortgage(self, owner):
        # check if owner has sufficient funds
        if not owner.balance >= self.mortgage: return messagebox.showerror("error", "Insufficient funds.")

        # repay the mortgage
        owner.adjustBalance(-self.mortgage)
        self.status = "active"
