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