import tkinter as tk
from libs.add_frame import AddFrame


class AddRentSplit(tk.Tk):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game

        # window parameters
        self.title("Add Rent Split")
        self.resizable(False, False)

        self.mainFrame = AddFrame(self)
        self.mainFrame.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        # focus on window
        self.focus_force()

        # run window
        self.mainloop()

    def addItem(self):
        name = self.mainFrame.getPName()
        pct = self.mainFrame.getPct()
        loc = self.mainFrame.getLoc()

        self.game.players[name].addRentSplit(pct, loc)
        if loc not in self.game.locations.keys():
            self.game.addLocation(loc)
        self.game.locations[loc].addRentSplit(name, pct)
        self.destroy()
