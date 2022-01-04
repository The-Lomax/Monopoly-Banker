import tkinter as tk
from tkinter import ttk


class MoneyFrame(tk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        pad = 5
        self.game = game
        self.controller = container

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
            text="Apply discount for: "
        )
        self.dCheckBox.grid(row=2, column=0, padx=pad, pady=pad)

        self.dBox = ttk.Combobox(
            self,
            state="readonly"
        )
        self.dBox.grid(row=2, column=1, padx=pad, pady=pad)

        self.rsCheckBox = tk.Checkbutton(
            self,
            text="Apply split for: "
        )
        self.rsCheckBox.grid(row=3, column=0, padx=pad, pady=pad)

        self.rsBox = ttk.Combobox(
            self,
            state="readonly"
        )
        self.rsBox.grid(row=3, column=1, padx=pad, pady=pad)

        self.mButton = tk.Button(
            self,
            text="Save",
            pady=pad,
            command=self.moveMoney,
            width=pad * 2
        )
        self.mButton.grid(row=4, column=0, columnspan=2, pady=pad)

        self.pack(fill="both", expand=True, padx=pad, pady=pad)

        self.pBox.bind("<<ComboboxSelected>>", self.loadPlayerRebates)

    def loadPlayerRebates(self, event):
        player = self.game.players[self.pBox.get()]
        discList = [el[0] for el in player.discounts]
        rsList = [el[0] for el in player.rentSplits]
        self.dBox["values"] = discList
        self.rsBox["values"] = rsList

    def moveMoney(self):
        target = self.game.players[self.pBox.get()]
        amt = int(self.aEntry.get())

        self.controller.moveMoney(target, amt)

        self.controller.controller.updateBadges()

        self.controller.exit()
