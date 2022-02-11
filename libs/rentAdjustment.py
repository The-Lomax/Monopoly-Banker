import tkinter as tk
from tkinter import ttk, messagebox


class RentAdjustmentFrame(tk.Frame):
    def __init__(self, container, game, mode, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game
        self.mode = mode

        pad = 5

        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(1, weight=1)

        # Labels
        tk.Label(self, text="Player: ").grid(row=0, column=0, padx=pad, pady=pad)
        tk.Label(self, text="Percentage: ").grid(row=1, column=0, padx=pad, pady=pad)
        tk.Label(self, text="Location: ").grid(row=2, column=0, padx=pad, pady=pad)

        # Entries
        self.pBox = ttk.Combobox(self)
        self.pBox.configure(state="readonly")
        self.pBox.grid(row=0, column=1, padx=pad)

        self.pctBox = tk.Entry(self, width=7)
        self.pctBox.grid(row=1, column=1, padx=pad)

        self.locBox = ttk.Combobox(self, width=20)
        self.locBox.grid(row=2, column=1, padx=pad)
        self.locBox.configure(state="readonly")
        self.locBox["values"] = [el for el in self.game.locations.keys()]

        # Buttons
        self.addBtn = tk.Button(self, text="Add", width=pad)
        self.addBtn.configure(command=self.addItem)
        self.addBtn.grid(row=3, column=0, columnspan=2, pady=pad)

        # read players to list
        self.readPlayers()

    def readPlayers(self):
        self.pBox['values'] = [el for el in self.game.players.keys()]

    def getPName(self):
        return self.pBox.get()

    def getPct(self):
        try:
            return int(self.pctBox.get())
        except ValueError:
            return 0

    def getLoc(self):
        return self.locBox.get()

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


    def addItem(self):
        name = self.mainFrame.getPName()
        pct = self.mainFrame.getPct()
        loc = self.mainFrame.getLoc()

        self.game.players[name].addDiscount(pct, loc)
        if loc not in self.game.locations.keys():
            self.game.addLocation(loc)
        self.game.locations[loc].addDiscount(name, pct)
        self.destroy()
