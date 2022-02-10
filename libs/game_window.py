import tkinter as tk
from tkinter import messagebox
from libs.add_discount import AddDiscount
from libs.add_rent_split import AddRentSplit
from libs.menu import GameMenu
from libs.playerFrame import PlayerList
from libs.add_player import AddPlayer
from libs.addEvent import AddEvent
from libs.locationFrame import LocationFrame
from libs.tradeFrame import TradeFrame
from libs.check_location import CheckLocation


class GameWindow(tk.Tk):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game
        self.game.mainWindow = self

        # window parameters
        self.title("Monopoly Banker")
        self.resizable(False, False)
        self.geometry(self.game.center(self, *(640, 480)))
        self.rowconfigure(0, weight=1)

        # menu setup
        self.menu = GameMenu(self)
        self.config(menu=self.menu)

        # main frame. This is the storage that will contain all the custom frames
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=0, column=0, sticky="news", padx=5, pady=5)

        # status bar
        self.statusBar = tk.Frame(self)
        self.statusLabel = tk.Label(
            self.statusBar,
            text="Status: ",
            font=("Helvetica", 13),
            anchor="w"
        )
        self.statusBar.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.statusLabel.pack(fill="x", expand=True)

        # frame elements
        self.playersFrame = PlayerList(self.mainFrame, self.game)
        self.addPlayerFrame = AddPlayer(self.mainFrame, self.game)
        self.addEventFrame = AddEvent(self.mainFrame, self.game)
        self.buildFrame = LocationFrame(self.mainFrame, self.game, "build")
        self.sellFrame = LocationFrame(self.mainFrame, self.game, "sell")
        self.mortgageFrame = LocationFrame(self.mainFrame, self.game, "mortgage")
        self.tradeLocFrame = TradeFrame(self.mainFrame, self.game)
        self.locInspectFrame = CheckLocation(self.mainFrame, self.game)
        self.addDiscountFrame = AddDiscount(self.mainFrame, self.game)
        self.addSplitFrame = AddRentSplit(self.mainFrame, self.game)

        # DEBUGGING

        # focus on window
        self.focus_force()

        # closing protocol
        self.protocol("WM_DELETE_WINDOW", self.safeExit)

        # run window
        self.showModule(self.playersFrame)
        self.mainloop()

    def showModule(self, module):
        self.hideAllFrames()
        module.grid(row=0, column=0, sticky="news")

    def hideAllFrames(self):
        for el in self.mainFrame.winfo_children():
            el.grid_forget()

    def safeExit(self):
        if messagebox.askyesno("Warning", "Are you sure?", parent=self):
            self.destroy()

    def addEvent(self, player):
        self.showModule(self.addEventFrame)
        self.addEventFrame.updateLabel(player)
