import tkinter as tk
from tkinter import ttk


class AddEvent(tk.Frame):
    def __init__(self, container, game, *args, player=None, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game
        self.player = player

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

        self.eventCheckBox = tk.Checkbutton(self, text="from everyone")

        self.saveButton = tk.Button(
            self,
            text="Save",
            width=8,
            command=self.saveEvent
        )
        self.saveButton.grid(row=2, column=0, columnspan=10)

        self.eventLocation.bind("<<ComboboxSelected>>", self.updateScreen)

    def updateScreen(self, e):
        if self.eventLocation.get() == "location":
            self.eventDestination['values'] = [el for el in self.game.locations.keys()]
        elif self.eventLocation.get() == "house":
            self.eventDestination['values'] = [el for el in self.game.houses.keys()]
        elif self.eventLocation.get() == "poi":
            self.eventDestination['values'] = [el for el in self.game.poi.keys()]
        elif self.eventLocation.get() == "card":
            self.eventDestination['values'] = ("pay", "collect")
            self.eventEntry.grid(row=1, column=3, padx=5, pady=5)
            self.eventCheckBox.grid(row=1, column=4, padx=5, pady=5)
        if not self.eventLocation.get() == "card":
            self.eventEntry.grid_forget()
            self.eventCheckBox.grid_forget()

    def saveEvent(self):
        #TODO data validation and processing and saving the event
        self.game.mainWindow.showModule(self.game.mainWindow.playersFrame)

    def updateLabel(self, player=None):
        if not player is None:
            self.player = player
            self.nameLabel['text'] = f"Player {player.name} lands on:"
