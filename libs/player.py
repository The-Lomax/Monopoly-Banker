from tkinter import messagebox


class Player:
    def __init__(self, pId, pName, pBal, pBkrupt):
        self.id = pId
        self.name = pName
        self.balance = pBal
        self.bankrupt = pBkrupt

    def adjustBalance(self, amt: int):
        self.balance += amt
        if self.balance < 0:
            self.goBankrupt()

    def isBankrupt(self) -> bool:
        if self.bankrupt:
            return True
        else:
            return False

    def goBankrupt(self) -> None:
        self.bankrupt = True
    
    def buy(self, location):
        # check if location is free and if not, stop executing
        if not location.status == "free": return messagebox.showerror("error", "Location is not available.")

        # check if buyer has sufficient funds and if not, stop executing
        if not self.balance >= location.buyPrice: return messagebox.showerror("error", "Insufficient funds.")

        self.adjustBalance(-location.buyPrice)
        location.status = "active"
        location.ownerId = self.id
