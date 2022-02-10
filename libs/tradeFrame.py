from distutils import command
import tkinter as tk
from tkinter import ttk


class TradeFrame(tk.Frame):
    def __init__(self, container, game, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)

        self.game = game

        self.p1Var = tk.BooleanVar()
        self.p2Var = tk.BooleanVar()

        tk.Label(
            self,
            text="trade",
            font=("Helvetica", 13)
        ).grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        self.leftSide = tk.Frame(self)
        self.leftSide.grid(row=1, column=0)
        self.leftSide.columnconfigure((0, 1), weight=1)
        self.leftSide.rowconfigure((0, 1, 2), weight=1)

        tk.Label(
            self.leftSide,
            text="P1: "
        ).grid(row=0, column=0)

        self.p1Box = ttk.Combobox(self.leftSide, width=5)
        self.p1Box.grid(row=0, column=1)

        tk.Label(
            self.leftSide,
            text="loc: "
        ).grid(row=1, column=0)

        self.p1Loc = ttk.Combobox(self.leftSide, width=5)
        self.p1Loc.grid(row=1, column=1)

        self.m1Check = tk.Checkbutton(
            self.leftSide,
            text="money:",
            variable=self.p1Var
        )
        self.m1Check.grid(row=2, column=0)

        self.m1Box = tk.Entry(self.leftSide, width=5)
        self.m1Box.grid(row=2, column=1)

        ttk.Separator(self, orient="vertical").grid(row=1, column=1, sticky="ns", padx=10)

        self.rightSide = tk.Frame(self)
        self.rightSide.grid(row=1, column=2)
        self.rightSide.columnconfigure((0, 1), weight=1)
        self.rightSide.rowconfigure((0, 1, 2), weight=1)

        tk.Label(
            self.rightSide,
            text="P2: "
        ).grid(row=0, column=0)

        self.p2Box = ttk.Combobox(self.rightSide, width=5)
        self.p2Box.grid(row=0, column=1)

        tk.Label(
            self.rightSide,
            text="loc: "
        ).grid(row=1, column=0)

        self.p2Loc = ttk.Combobox(self.rightSide, width=5)
        self.p2Loc.grid(row=1, column=1)

        self.m2Check = tk.Checkbutton(
            self.rightSide,
            text="money:",
            variable=self.p2Var
        )
        self.m2Check.grid(row=2, column=0)

        self.m2Box = tk.Entry(self.rightSide, width=5)
        self.m2Box.grid(row=2, column=1)

        tk.Button(
            self,
            text="save",
            padx=5,
            pady=5,
            command=self.saveTrade
        ).grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    def saveTrade(self):
        self.game.mainWindow.showModule(self.game.mainWindow.playersFrame)
    
