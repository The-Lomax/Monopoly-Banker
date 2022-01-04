import tkinter as tk
from libs.money_frame import MoneyFrame


class AddMoney(tk.Tk):
    def __init__(self, controller, player, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller
        self.game = controller.game
        self.origin = player

        # window parameters
        self.title(f"Add Money: {self.origin.name}")
        self.resizable(False, False)

        # main form
        self.mainFrame = MoneyFrame(self, self.game)

        # focus on window
        self.focus_force()

        # run window
        self.mainloop()

    def moveMoney(self, target, amount):
        self.origin.addFunds(amount)
        target.takeFunds(amount)

    def exit(self):
        self.destroy()
