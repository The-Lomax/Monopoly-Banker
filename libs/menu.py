import tkinter as tk
from libs.add_player import AddPlayer
from libs.add_discount import AddDiscount
from libs.add_rent_split import AddRentSplit
from libs.check_location import CheckLocation


class GameMenu(tk.Menu):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = container

        mGame = tk.Menu(self, tearoff=0)

        mGame.add_command(label="Add Player", command=self.openAddPlayerWindow)
        mGame.add_separator()
        mGame.add_command(label="Reset Game", command=self.controller.game.resetGameState)
        mGame.add_separator()
        mGame.add_command(label="Exit", command=self.controller.safeExit)

        mPlayer = tk.Menu(self, tearoff=0)
        mPlayer.add_command(label="Add discount", command=self.openAddDiscountWindow)
        mPlayer.add_separator()
        mPlayer.add_command(label="Add rent split", command=self.openAddRentSplitWindow)

        mLocation = tk.Menu(self, tearoff=0)
        mLocation.add_command(label="Check...", command=self.openLocationCheckWindow)

        self.add_cascade(label="Game", menu=mGame)
        self.add_cascade(label="Player", menu=mPlayer)
        self.add_cascade(label="Location", menu=mLocation)

    def openAddPlayerWindow(self):
        self.controller.showModule(self.controller.addPlayerFrame)

    def openAddDiscountWindow(self):
        AddDiscount(self.controller.game)

    def openAddRentSplitWindow(self):
        AddRentSplit(self.controller.game)

    def openLocationCheckWindow(self):
        CheckLocation(self.controller.game)