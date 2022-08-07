import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class CheckLocation(tk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game
        self.pad = 5

        # window parameters
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Top row with combobox and button
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=0, column=0, sticky="new", padx=self.pad, pady=self.pad)
        self.mainFrame.columnconfigure(1, weight=1)

        tk.Label(
            self.mainFrame, text="Location: "
        ).grid(row=0, column=0, padx=self.pad, pady=self.pad)

        self.locBox = ttk.Combobox(self.mainFrame)
        self.locBox.configure(state="readonly")
        self.locBox.grid(row=0, column=1, sticky="ew", padx=self.pad, pady=self.pad)

        self.loadBtn = tk.Button(
            self.mainFrame, text="Load", padx=self.pad, width=5, command=self.loadLoc
        )
        self.loadBtn.grid(row=0, column=2, sticky="e", padx=self.pad, pady=self.pad)

        self.infoFrame = tk.Frame(self)
        self.infoFrame.grid(row=1, column=0, sticky="new", padx=self.pad, pady=self.pad)

        # Info labels
        self.stateLabel = tk.Label(
            self.infoFrame, text="Status: ", font=("Helvetica", 12), anchor="w"
        )
        self.stateLabel.grid(row=0, column=0, sticky="new", padx=self.pad, pady=self.pad)

        self.ownerLabel = tk.Label(
            self.infoFrame, text="Owner: ", font=("Helvetica", 12), anchor="w"
        )
        self.ownerLabel.grid(row=1, column=0, sticky="new", padx=self.pad, pady=self.pad)

        self.buildingsLabel = tk.Label(
            self.infoFrame, text="Buildings: ", font=("Helvetica", 12), anchor="w"
        )
        self.buildingsLabel.grid(row=2, column=0, sticky="new", padx=self.pad, pady=self.pad)

        # Discounts label
        self.secondFrame = tk.Frame(self)
        self.secondFrame.grid(row=2, column=0, sticky="new", padx=self.pad, pady=self.pad)

        tk.Label(
            self.secondFrame, text="Discounts:", anchor="w"
        ).grid(sticky="new", padx=self.pad, pady=self.pad)

        # List of discounts
        self.thirdFrame = tk.Frame(self)
        self.thirdFrame.grid(row=3, column=0, sticky="new", padx=self.pad, pady=self.pad)

        # Splits label
        self.fourthFrame = tk.Frame(self)
        self.fourthFrame.grid(row=4, column=0, sticky="new", padx=self.pad, pady=self.pad)

        tk.Label(
            self.fourthFrame, text="Rent Splits:"
        ).grid(sticky="new", padx=self.pad, pady=self.pad)

        # List of splits
        self.fifthFrame = tk.Frame(self)
        self.fifthFrame.grid(row=5, column=0, sticky="new", padx=self.pad, pady=self.pad)

        # exit button
        tk.Button(
            self, text="exit", width=5, padx=5, pady=5, command=self.exitFrame
        ).grid(row=6, column=0, columnspan=10, padx=5, pady=5)

        # read locations into the combobox
        self.readLocations()
    
    def exitFrame(self):
        self.game.mainWindow.showModule(self.game.mainWindow.playersFrame)

    def readLocations(self):
        keys = [el.name for el in self.game.locations.values()] + [el.name for el in self.game.houses.values()] + [el.name for el in self.game.poi.values()]
        self.locBox['values'] = keys

    def loadLoc(self):
        # clear the list
        for el in self.thirdFrame.winfo_children(): el.destroy()
        for el in self.fifthFrame.winfo_children(): el.destroy()

        # read location name off the list
        locName = self.locBox.get()

        # stop executing if location not selected
        if locName == "": return messagebox.showerror("error", "error! Please choose a location.", parent=self)

        # assign location object
        if locName in self.game.locations.keys(): loc = self.game.locations[locName]
        elif locName in self.game.houses.keys(): loc = self.game.houses[locName]
        else: loc = self.game.poi[locName]

        # assign location owner
        try:
            owner = loc.locateOwner(self.game.players).name
        except AttributeError:
            owner = 'Bank'

        # update info labels
        self.stateLabel.configure(text=f"Status: {loc.status}")
        self.ownerLabel.configure(text=f"Owner: {owner}")

        # update buildings, discounts and splits if location selected (not a house and not a POI)
        if loc.name in self.game.locations.keys():
            self.buildingsLabel.configure(text=f"Buildings: {loc.buildings}")
            
            if len(loc.discounts) > 0:
                for player, pct in self.game.locations[locName].discounts.items():
                    tk.Label(
                        self.thirdFrame, text=f"{player} - {pct}%"
                    ).pack(fill="x", padx=self.pad, pady=(self.pad, 0))
            else:
                tk.Label(
                    self.thirdFrame, text="No discounts found."
                ).pack(fill="x", padx=self.pad, pady=(self.pad, 0))

            if len(loc.rentSplits) > 0:
                for player, pct in self.game.locations[locName].rentSplits.items():
                    tk.Label(
                        self.fifthFrame, text=f"{player} - {pct}%"
                    ).pack(fill="x", padx=self.pad, pady=(self.pad, 0))
            else:
                tk.Label(
                    self.fifthFrame, text="No rent splits found."
                ).pack(fill="x", padx=self.pad, pady=(self.pad, 0))
