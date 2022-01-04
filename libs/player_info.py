import tkinter as tk


class PlayerInfo(tk.Tk):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player = player
        self.pad = 5

        # window parameters
        self.title(f"Player info: {self.player.name}")
        self.resizable(False, False)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Top row with balance
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=0, column=0, sticky="new", padx=self.pad, pady=self.pad)
        self.mainFrame.columnconfigure(1, weight=1)

        self.pBal = tk.Label(
            self.mainFrame,
            text=f"Balance: $ 0"
        )
        self.pBal.grid(sticky="new", padx=self.pad, pady=self.pad)

        # Discounts label
        self.secondFrame = tk.Frame(self)
        self.secondFrame.grid(row=1, column=0, sticky="new", padx=self.pad, pady=self.pad)

        tk.Label(
            self.secondFrame,
            text="Discounts:"
        ).grid(sticky="new", padx=self.pad, pady=self.pad)

        # List of discounts
        self.thirdFrame = tk.Frame(self)
        self.thirdFrame.grid(row=2, column=0, sticky="new", padx=self.pad, pady=self.pad)

        # Splits label
        self.fourthFrame = tk.Frame(self)
        self.fourthFrame.grid(row=3, column=0, sticky="new", padx=self.pad, pady=self.pad)

        tk.Label(
            self.fourthFrame,
            text="Rent Splits:"
        ).grid(sticky="new", padx=self.pad, pady=self.pad)

        # List of splits
        self.fifthFrame = tk.Frame(self)
        self.fifthFrame.grid(row=4, column=0, sticky="new", padx=self.pad, pady=self.pad)

        # load player info
        self.loadInfo()

        # focus on window
        self.focus_force()

        # run window
        self.mainloop()

    def loadInfo(self):
        # clear the list
        for el in self.thirdFrame.winfo_children():
            el.destroy()
        for el in self.fifthFrame.winfo_children():
            el.destroy()

        # update balance
        self.pBal.configure(text=f"Balance: $ {self.player.balance}")

        # update discounts
        if len(self.player.discounts) > 0:
            for loc, pct in self.player.discounts.items():
                tk.Label(
                    self.thirdFrame,
                    text=f"{loc} - {pct}%"
                ).pack(
                    fill="x",
                    padx=self.pad,
                    pady=(self.pad, 0)
                )
        else:
            tk.Label(
                self.thirdFrame,
                text="No discounts found."
            ).pack(
                fill="x",
                padx=self.pad,
                pady=(self.pad, 0)
            )

        # update rent splits
        if len(self.player.rentSplits) > 0:
            for loc, pct in self.player.rentSplits.items():
                tk.Label(
                    self.fifthFrame,
                    text=f"{loc} - {pct}%"
                ).pack(
                    fill="x",
                    padx=self.pad,
                    pady=(self.pad, 0)
                )
        else:
            tk.Label(
                self.fifthFrame,
                text="No rent splits found."
            ).pack(
                fill="x",
                padx=self.pad,
                pady=(self.pad, 0)
            )
