import tkinter as tk
from tkinter import messagebox
from libs.menu import GameMenu
from libs.playerFrame import PlayerList
from libs.add_player import AddPlayer
from libs.addEvent import AddEvent


class GameWindow(tk.Tk):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game
        self.game.mainWindow = self

        # window parameters
        self.title("Monopoly Banker")
        self.resizable(False, False)
        self.geometry(self.game.center(self, *(640, 480)))

        # menu setup
        self.menu = GameMenu(self)
        self.config(menu=self.menu)

        # main frame. This is the storage that will contain all the custom frames
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill="both", expand="True", padx=5, pady=5)

        # players frame
        self.playersFrame = PlayerList(self.mainFrame, self.game)
        self.addPlayerFrame = AddPlayer(self.mainFrame, self.game)
        self.addEventFrame = AddEvent(self.mainFrame, self.game)

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
        module.grid(row=0, column=0, sticky="new")

    def hideAllFrames(self):
        for el in self.mainFrame.winfo_children():
            el.grid_forget()

    def safeExit(self):
        if messagebox.askyesno("Warning", "Are you sure?", parent=self):
            self.destroy()

    def addEvent(self, player):
        self.showModule(self.addEventFrame)
        self.addEventFrame.updateLabel(player)
