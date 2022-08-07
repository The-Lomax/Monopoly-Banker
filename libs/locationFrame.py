import tkinter as tk
from tkinter import ttk, messagebox


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
        self.locBox["state"] = "readonly"
        self.locBox.grid(row=1, column=1, padx=5, pady=5)

        self.pLabel = tk.Label(
            self,
            text="",
            font=("Helvetica", 12)
        )

        self.pBox = tk.Entry(self, width=10)

        self.pList = ttk.Combobox(self, width=10)
        self.pList["state"] = "readonly"

        if not self.mode == "mortgage":
            self.pLabel.grid(row=2, column=0, padx=5, pady=5)
            if self.mode == "build" or self.mode == "bulldoze":
                self.pLabel.configure(text="#: ")
                self.pBox.grid(row=2, column=1, padx=5, pady=5)
            elif self.mode == "sell":
                self.pLabel.configure(text="Player: ")
                self.pList.grid(row=2, column=1, padx=5, pady=5)

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
        # read location name from the checkbox
        location = self.locBox.get()

        # stop executing the function if location not selected
        if location == "": return messagebox.showerror("error", "Select a location.", parent=self)

        # assign location object
        if location in self.game.locations.keys():
            loc = self.game.locations[location]
        elif location in self.game.houses.keys():
            loc = self.game.houses[location]
        else:
            loc = self.game.poi[location]

        # process the event
        if self.mode == "build":
            # read number of buildings
            try:
                buildAmt = int(self.pBox.get())
            except ValueError:
                buildAmt = 0
            
            # build number of items on the location
            loc.build(self.game.players, buildAmt)
        elif self.mode == "bulldoze":
            # read number of buildings
            try:
                buildAmt = int(self.pBox.get())
            except ValueError:
                buildAmt = 0
            
            # bulldoze number of items on the location
            loc.bulldoze(self.game.players, buildAmt)
        elif self.mode == "sell":
            # read player information from the list
            buyer = self.pList.get()

            # stop executing if player not selected
            if buyer == "": return messagebox.showerror("error", "Select a player.", parent=self)

            #
            buyer = self.game.players[buyer]

            # process the event
            buyer.buy(loc)

            self.game.savePlayerInfo(buyer)
        else:  # mortgage
            loc.toggleMortgage(self.game.players)

        # return back to the player list
        self.locBox.set("")
        self.pBox.delete(0, "end")
        self.pList.set("")

        self.game.saveLocationInfo(loc)

        self.game.returnToMain()
    
    def refreshData(self):
        if self.mode == "build":
            self.locBox["values"] = [el.name for el in self.game.locations.values() if el.status == "active"]
        elif self.mode == "bulldoze":
            self.locBox["values"] = [el.name for el in self.game.locations.values() if el.buildings > 0]
        elif self.mode == "sell":
            self.locBox["values"] = [el.name for el in self.game.locations.values() if el.status == "free"] + [el.name for el in self.game.houses.values() if el.status == "free"] + [el.name for el in self.game.poi.values() if el.status == "free"]
            self.pList["values"] = [el.name for el in self.game.players.values()]
        else:  # mortgage
            self.locBox["values"] = [el.name for el in self.game.locations.values() if el.status == "active" or el.status == "mortgaged"] + [el.name for el in self.game.houses.values() if el.status == "active" or el.status == "mortgaged"] + [el.name for el in self.game.poi.values() if el.status == "active" or el.status == "mortgaged"]