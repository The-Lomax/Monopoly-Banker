import tkinter as tk
import math
from tkinter import ttk, messagebox


class AddEvent(tk.Frame):
    def __init__(self, container, game, *args, player=None, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game
        self.player = player
        self.eventVar = tk.BooleanVar()

        tk.Label(
            self,
            text="Add Event"
        ).grid(row=0, column=0, columnspan=5)

        self.nameLabel = tk.Label(
            self,
            text=f"event info goes here"
        )
        self.nameLabel.grid(row=1, column=0, padx=5, pady=5)

        self.eventLocation = ttk.Combobox(self, width=20)
        self.eventLocation['values'] = ("location", "house", "poi", "card")
        self.eventLocation['state'] = "readonly"
        self.eventLocation.grid(row=1, column=1, padx=5, pady=5)

        self.eventDestination = ttk.Combobox(self, width=20)
        self.eventDestination['values'] = ("locations", "go", "here")
        self.eventDestination['state'] = "readonly"
        self.eventDestination.grid(row=1, column=2, padx=5, pady=5)

        self.eventEntry = tk.Entry(self, width=5)

        self.eventCheckBox = tk.Checkbutton(self, text="from players", variable=self.eventVar)

        self.saveButton = tk.Button(
            self,
            text="Save",
            width=8,
            command=self.saveEvent
        )
        self.saveButton.grid(row=2, column=0, columnspan=10)

        self.eventLocation.bind("<<ComboboxSelected>>", self.updateScreen)

    def updateScreen(self, e):
        self.eventDestination.set("")
        if self.eventLocation.get() == "location":
            self.eventDestination['values'] = [el.name for el in self.game.locations.values() if el.status == "active"]
        elif self.eventLocation.get() == "house":
            self.eventDestination['values'] = [el.name for el in self.game.houses.values() if el.status == "active"]
        elif self.eventLocation.get() == "poi":
            self.eventDestination['values'] = [el.name for el in self.game.poi.values() if el.status == "active"]
            self.eventEntry.grid(row=1, column=3, padx=5, pady=5)
        elif self.eventLocation.get() == "card":
            self.eventDestination['values'] = ("pay", "collect")
            self.eventEntry.grid(row=1, column=3, padx=5, pady=5)
            self.eventCheckBox.grid(row=1, column=4, padx=5, pady=5)
        if not self.eventLocation.get() in ("card", "poi"):
            self.eventEntry.grid_forget()
        if not self.eventLocation.get() == "card":
            self.eventCheckBox.grid_forget()

    def saveEvent(self):
        # get the location and category
        locType = self.eventLocation.get()
        locName = self.eventDestination.get()

        # exit the function if either not selected
        if locType == "" or locName == "": return messagebox.showerror("error", "Check your input.", parent=self)

        # assign location object
        if locType == "location":
            loc = self.game.locations[locName]
        elif locType == "house":
            loc = self.game.houses[locName]
        elif locType == "poi":
            loc = self.game.poi[locName]
        elif locType == "card":
            pass
        
        # exit the function if location is unowned or mortgaged
        if not locType == "card":
            if not loc.status == "active": return messagebox.showerror("error", "Location mortgaged or unowned.", parent=self)

        # assign guest and owner
        guest = self.player
        if not locType == "card":
            owner = loc.locateOwner(self.game.players)

        # get the number figure
        diceRoll = 0
        amount = 0
        if locType == "poi":
            try:
                diceRoll = int(self.eventEntry.get())
            except ValueError:
                diceRoll = 0
        elif locType == "card":
            try:
                amount = int(self.eventEntry.get())
            except ValueError:
                amount = 0

        # get the bill amount
        bill = 0
        counter = 0
        if locType == "location":
            bill = loc.rent[loc.buildings]
        elif locType == "house":
            for el in self.game.houses.values():
                if el.ownerId == owner.id:
                    counter += 1
            if counter > 0:
                bill = loc.rent[counter - 1]
            else:
                bill = loc.rent[counter]
        elif locType == "poi":
            for el in self.game.poi.values():
                if el.ownerId == owner.id:
                    counter += 1
            if counter > 0:
                bill = loc.rent[counter - 1]
            else:
                bill = loc.rent[counter]
            bill *= diceRoll

        # process rent if not location
        # guest draws card
        if locType == "card":
            # card says PAY
            if locName == "pay":
                # card says from everyone
                if self.eventVar.get():
                    counter = 0
                    for el in self.game.players.values():
                        if not el.id == guest.id:
                            el.adjustBalance(amount)
                            counter += 1
                    guest.adjustBalance(-(amount * counter))
                # or not
                else:
                    guest.adjustBalance(-amount)
            # card says COLLECT
            elif locName == "collect":
                # card says from everyone
                if self.eventVar.get():
                    counter = 0
                    for el in self.game.players.values():
                        if not el.id == guest.id:
                            el.adjustBalance(-amount)
                            counter += 1
                            self.game.savePlayerInfo(el)
                    guest.adjustBalance(amount * counter)
                # or not
                else:
                    guest.adjustBalance(amount)
        elif locType in ("poi", "house"):
            guest.adjustBalance(-bill)
            owner.adjustBalance(bill)
        # calculate rent for location
        else:
            # reduce rent if guest has a discount
            if guest.name in loc.discounts.keys():
                bill = bill - math.floor(bill * (loc.discounts[guest.name] / 100))
            
            if bill > 0:
                # charge the guest
                guest.adjustBalance(-bill)
                
                # calculate the rent splits if any
                if len(loc.rentSplits.keys()) > 0:
                    deduction = 0
                    for p, v in loc.rentSplits.items():
                        amt = math.floor(bill * (v / 100))
                        self.game.players[p].adjustBalance(amt)
                        deduction += amt
                    owner.adjustBalance(bill - deduction)
                else:
                    owner.adjustBalance(bill)

        # clean up
        self.eventLocation.set("")
        self.eventDestination.set("")
        self.eventEntry.delete(0, "end")
        self.eventVar.set(False)

        if locType == "card":
            self.game.savePlayerInfo(guest)
        else:
            self.game.savePlayerInfo(guest)
            self.game.savePlayerInfo(owner)

        self.game.returnToMain()

    def updateLabel(self, player=None):
        if not player is None:
            self.player = player
            self.nameLabel['text'] = f"Player {player.name} lands on:"
