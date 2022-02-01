import tkinter as tk
from tkinter import messagebox
from libs.menu import GameMenu
from libs.playerFrame import PlayerFrame


class GameWindow(tk.Tk):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game

        # window parameters
        self.title("Monopoly Banker")
        self.resizable(False, False)
        self.geometry(self.game.center_app(self, *(640, 480)))

        # menu setup
        self.menu = GameMenu(self)
        self.config(menu=self.menu)

        # main frame. This is the storage that will contain all the custom frames
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill="both", expand="True", padx=5, pady=5)

        # players frame
        self.playersFrame = tk.Frame(self)

        # DEBUGGING

        # focus on window
        self.focus_force()

        # closing protocol
        self.protocol("WM_DELETE_WINDOW", self.safeExit)

        # run window
        self.mainloop()

    def updateBadges(self):
        for el in self.mainFrame.winfo_children():
            if el.winfo_class() == "Frame":
                el.destroy()

        # create player badges
        pad = 5
        for name, player in self.game.players.items():
            if not player.isBankrupt():
                PlayerBadge(self, player).pack(fill="x", expand=True, padx=pad, pady=(pad, 0))
        self.geometry(f"300x{30 * len(self.winfo_children()) + 50}")

    def safeExit(self):
        if messagebox.askyesno("Warning", "Are you sure?", parent=self):
            self.destroy()
