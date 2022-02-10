import tkinter as tk
from libs.add_frame import AddFrame


class AddDiscount(tk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game

        self.mainFrame = AddFrame(self)
        self.mainFrame.grid(row=0, column=0, sticky="new", padx=5, pady=5)

    def addItem(self):
        name = self.mainFrame.getPName()
        pct = self.mainFrame.getPct()
        loc = self.mainFrame.getLoc()

        self.game.players[name].addDiscount(pct, loc)
        if loc not in self.game.locations.keys():
            self.game.addLocation(loc)
        self.game.locations[loc].addDiscount(name, pct)
        self.destroy()
