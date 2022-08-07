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

        # Buttons
        self.addBtn = tk.Button(self, text="Add", width=pad)
        self.addBtn.configure(command=self.addItem)
        self.addBtn.grid(row=3, column=0, columnspan=2, pady=pad)

        # update data
        self.updateInfo()

    def updateInfo(self):
        self.pBox['values'] = [el for el in self.game.players.keys()]
        self.locBox["values"] = [el.name for el in self.game.locations.values() if not el.status == "free"]

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
        name = self.getPName()
        if name == "": return messagebox.showerror("error", f"Player not selected.", parent=self)

        pct = self.getPct()
        if pct <= 0: return messagebox.showerror("error", f"Discount must be greater than 0%.", parent=self)

        loc = self.getLoc()

        # assign location object
        loc = self.game.locations[loc]

        if self.game.players[name].id == loc.ownerId:
            return messagebox.showerror("error", f"Cannot add discount/split for the location owner.", parent=self)

        if self.mode == "discount":
            loc.addDiscount(name, pct)
        elif self.mode == "split":
            res = 0
            for el in loc.rentSplits.values():
                res += el
                
            if res + pct > 100:
                return messagebox.showerror("error", f"Collective rent split cannot be higher than 100%. Your limit is {100 - res}%. Correct the split amount.", parent=self)
            
            loc.addRentSplit(name, pct)
        
        # clean up
        self.pBox.set("")
        self.locBox.set("")
        self.pctBox.delete(0, "end")

        self.game.saveLocationInfo(loc)
        
        self.game.returnToMain()
