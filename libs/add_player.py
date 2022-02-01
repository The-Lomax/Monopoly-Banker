import tkinter as tk
from tkinter import messagebox


class AddPlayer(tk.Tk):
    def __init__(self, controller, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game
        self.controller = controller
        pad = 5

        # window parameters
        self.title("Add Player")
        self.resizable(False, False)

        self.mainFrame = tk.Frame(self)
        self.mainFrame.rowconfigure((0, 1, 2), weight=1)
        self.mainFrame.columnconfigure((1, 2), weight=1)
        self.mainFrame.pack()

        # Labels
        tk.Label(
            self.mainFrame,
            text="Player name: "
        ).grid(
            row=0, column=0,
            padx=pad, pady=pad
        )

        tk.Label(
            self.mainFrame,
            text="Starting balance: "
        ).grid(
            row=1, column=0,
            padx=pad, pady=pad
        )

        # Entries
        self.pName = tk.Entry(self.mainFrame, width=20)
        self.pName.grid(row=0, column=1, sticky="new", padx=pad, pady=pad)

        self.sBal = tk.Entry(self.mainFrame, width=20)
        self.sBal.grid(row=1, column=1, sticky="new", padx=pad, pady=pad)

        # Buttons
        self.addBtn = tk.Button(
            self.mainFrame,
            text="Add",
            command=self.addItem,
            width=5,
            pady=pad
        )
        self.addBtn.grid(row=2, column=0, columnspan=2, pady=pad)

        # focus on window
        self.pName.focus_force()

        # run window
        self.mainloop()

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

        self.game.addPlayer(self.game.pCount + 1, name, bal, False)
        self.controller.updateBadges()
        self.destroy()
