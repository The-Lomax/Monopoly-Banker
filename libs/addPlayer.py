import tkinter as tk
from tkinter import messagebox


class AddPlayer(tk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game
        pad = 5

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((1, 2), weight=1)

        # Labels
        tk.Label(
            self,
            text="Player name: "
        ).grid(
            row=0, column=0,
            padx=pad, pady=pad
        )

        tk.Label(
            self,
            text="Starting balance: "
        ).grid(
            row=1, column=0,
            padx=pad, pady=pad
        )

        # Entries
        self.pName = tk.Entry(self, width=20)
        self.pName.grid(row=0, column=1, sticky="new", padx=pad, pady=pad)

        self.sBal = tk.Entry(self, width=20)
        self.sBal.grid(row=1, column=1, sticky="new", padx=pad, pady=pad)

        # Buttons
        self.addBtn = tk.Button(
            self,
            text="Add",
            command=self.addItem,
            width=5,
            pady=pad
        )
        self.addBtn.grid(row=2, column=0, columnspan=2, pady=pad)

        # focus on window
        self.pName.focus_force()

    def addItem(self):
        name = self.pName.get()
        if name == "":
            messagebox.showerror("error", "Player name cannot be empty!", parent=self)
            return
        try:
            bal = int(self.sBal.get())
        except ValueError:
            messagebox.showerror("error", "Check the balance!", parent=self)
            return

        self.game.createPlayer(self.game.pCount + 1, name, bal, False)
        self.pName.delete(0, "end")
        self.sBal.delete(0, "end")
        self.game.loadPlayersFromWeb()
        self.game.mainWindow.showModule(self.game.mainWindow.playersFrame)
        self.game.mainWindow.playersFrame.loadPlayers()
