from libs.player import Player
from libs.location import Location


class Game:
    def __init__(self):
        self.pCount = 0
        self.lCount = 0
        self.players = {}
        self.locations = {}

    def setPlayers(self, pNumber: int) -> None:
        self.pCount = pNumber

    def addPlayer(self, pName: str, pBal: int) -> None:
        self.players[pName] = Player(pName, pBal)
        self.pCount += 1

    def addLocation(self, loc: str) -> None:
        self.locations[loc] = Location(loc)
        self.lCount += 1
