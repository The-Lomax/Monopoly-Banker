import tkinter as tk
from tkinter import messagebox
from libs.addPlayer import AddPlayer
from libs.addEvent import AddEvent
from libs.checkLocation import CheckLocation
from libs.locationFrame import LocationFrame
from libs.menu import GameMenu
from libs.playerFrame import PlayerList
from libs.rentAdjustment import RentAdjustmentFrame
from libs.tradeFrame import TradeFrame


class GameWindow(tk.Tk):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game
        self.game.mainWindow = self

        # window parameters
        self.title("Monopoly Banker")
        self.resizable(False, False)
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
        self.addDiscountFrame = RentAdjustmentFrame(self.mainFrame, self.game, "discount")
        self.addSplitFrame = RentAdjustmentFrame(self.mainFrame, self.game, "split")
        self.bulldozeLocationFrame = LocationFrame(self.mainFrame, self.game, "bulldoze")

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
