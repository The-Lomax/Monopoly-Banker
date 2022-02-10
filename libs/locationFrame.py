import tkinter as tk
from tkinter import ttk


class LocationFrame(tk.Frame):
    def __init__(self, container, game, mode, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)

        self.game = game
        self.mode = mode

        self.columnconfigure((0, 1), weight=1)

        tk.Label(
            self,
            text=self.mode,
            font=("Helvetica", 13)
        ).grid(row=0, column=0, columnspan=10, padx=5, pady=5)

        tk.Label(
            self,
            text="Location: "
        ).grid(row=1, column=0, padx=5, pady=5)

        self.locBox = ttk.Combobox(self)
        self.locBox.grid(row=1, column=1, padx=5, pady=5)

        self.pLabel = tk.Label(
            self,
            text="",
            font=("Helvetica", 12)
        )

        self.pBox = tk.Entry(self, width=10)

        self.pCheckbox = ttk.Combobox(self, width=10)

        if not self.mode == "mortgage":
            self.pLabel.grid(row=2, column=0, padx=5, pady=5)
            if self.mode == "build":
                self.pLabel.configure(text="#: ")
                self.pBox.grid(row=2, column=1, padx=5, pady=5)
            elif self.mode == "sell":
                self.pLabel.configure(text="Player: ")
                self.pCheckbox.grid(row=2, column=1, padx=5, pady=5)

        self.saveBtn = tk.Button(
            self,
            text="Save",
            command=self.saveEvent,
            padx=5,
            pady=5
        )
        self.saveBtn.grid(row=3, column=0, columnspan=10, padx=5, pady=5)

        self.refreshData()

    def saveEvent(self):
        self.game.mainWindow.showModule(self.game.mainWindow.playersFrame)
    
    def refreshData(self):
        self.locBox["values"] = [el.name for el in self.game.locations.values()] + [el.name for el in self.game.houses.values()] + [el.name for el in self.game.poi.values()]
        self.pCheckbox["values"] = [el.name for el in self.game.players.values()]