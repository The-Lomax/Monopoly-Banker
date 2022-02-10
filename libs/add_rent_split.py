import tkinter as tk
from tkinter import messagebox
from libs.add_frame import AddFrame


class AddRentSplit(tk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game

        self.mainFrame = AddFrame(self)
        self.mainFrame.grid(row=0, column=0, sticky="new", padx=5, pady=5)

    def addItem(self):
        name = self.mainFrame.getPName()
        pct = self.mainFrame.getPct()
        loc = self.mainFrame.getLoc()

        res = 0
        if loc in self.game.locations.keys():
            for el in self.game.locations[loc].rentSplits.values():
                res += el
            
        if res + pct > 100:
            messagebox.showerror("error", f"Collective rent split cannot be higher than 100%. Your limit is {100 - res}%. Correct the split amount.")
            return

        self.game.players[name].addRentSplit(pct, loc)
        if loc not in self.game.locations.keys():
            self.game.addLocation(loc)
        self.game.locations[loc].addRentSplit(name, pct)
        self.destroy()
