import tkinter as tk
from tkinter import ttk, messagebox


class MoneyFrame(tk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        pad = 5
        self.game = game
        self.controller = container
        self.dCB = False

        tk.Label(
            self,
            text="Target: "
        ).grid(row=0, column=0, padx=pad, pady=pad)

        players = [el for el in self.game.players.keys()]
        self.pBox = ttk.Combobox(
            self,
            values=players,
            state="readonly"
        )
        self.pBox.grid(row=0, column=1, padx=pad, pady=pad)

        tk.Label(
            self,
            text="Amount: "
        ).grid(row=1, column=0, padx=pad, pady=pad)

        self.aEntry = tk.Entry(
            self,
            width=pad * 2
        )
        self.aEntry.insert(0, 0)
        self.aEntry.grid(row=1, column=1, padx=pad, pady=pad)

        self.dCheckBox = tk.Checkbutton(
            self,
            text="Apply discounts for: ",
            variable=self.dCB,
            onvalue=1,
            offvalue=0,
            command=self.toggleState
        )
        self.dCheckBox.grid(row=2, column=0, padx=pad, pady=pad)

        self.dBox = ttk.Combobox(
            self,
            state="readonly"
        )
        self.dBox.grid(row=2, column=1, padx=pad, pady=pad)

        self.mButton = tk.Button(
            self,
            text="Save",
            pady=pad,
            command=self.moveMoney,
            width=pad * 2
        )
        self.mButton.grid(row=3, column=0, columnspan=2, pady=pad)

        self.pack(fill="both", expand=True, padx=pad, pady=pad)

        self.loadPlayerRebates()
    
    def toggleState(self):
        self.dCB = not self.dCB

    def loadPlayerRebates(self):
        locList = [el for el in self.game.locations.keys()]
        self.dBox["values"] = locList

    def moveMoney(self):
        _from = self.game.players[self.pBox.get()]
        _to = self.controller.origin

        amt = int(self.aEntry.get())

        deduction = 0

        # apply discount if valid
        if self.dCB:
            loc = self.dBox.get()
            if loc == "":
                messagebox.showerror("error", "Please select a location or uncheck the box.", parent=self)
                return
            pct = _from.checkRebate(_from.discounts, loc)
            amt *= (100 - pct) / 100

            for player, split in self.game.locations[loc].rentSplits.items():
                splitAmt = amt * split // 100
                self.controller.moveMoney(_from, self.game.players[player], splitAmt)
                deduction += splitAmt

        self.controller.moveMoney(_from, _to, amt - deduction)

        self.controller.controller.updateBadges()

        self.controller.exit()
