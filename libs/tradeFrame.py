import tkinter as tk
from tkinter import ttk, messagebox


class TradeFrame(tk.Frame):
    def __init__(self, container, game, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)

        self.game = game

        self.p1Var = tk.BooleanVar()
        self.p2Var = tk.BooleanVar()

        self.p1 = None
        self.p2 = None

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

        self.p1Box = ttk.Combobox(self.leftSide, width=10, state="readonly")
        self.p1Box.grid(row=0, column=1)

        tk.Label(
            self.leftSide,
            text="loc: "
        ).grid(row=1, column=0)

        self.p1Loc = ttk.Combobox(self.leftSide, width=10, state="readonly")
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

        self.p2Box = ttk.Combobox(self.rightSide, width=10, state="readonly")
        self.p2Box.grid(row=0, column=1)

        tk.Label(
            self.rightSide,
            text="loc: "
        ).grid(row=1, column=0)

        self.p2Loc = ttk.Combobox(self.rightSide, width=10, state="readonly")
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

        self.p1Box.bind("<<ComboboxSelected>>", self.loadP1Locations)
        self.p2Box.bind("<<ComboboxSelected>>", self.loadP2Locations)

        self.savePlayerLists()

    def saveTrade(self):
        # exit if players not selected
        if self.p1Box.get() == "" or self.p2Box.get() == "": return messagebox.showerror("error", "Players not selected.", parent=self)

        # swap locations if selected
        loc1 = self.p1Loc.get()
        if not loc1 == "":
            loc1 = self.game.locations[loc1]
            loc1.setOwnership(self.p2)
        
        loc2 = self.p2Loc.get()
        if not loc2 == "":
            loc2 = self.game.locations[loc2]
            loc2.setOwnership(self.p1)
        
        # check if money is involved and process payments
        m1money = 0
        m2money = 0
        if self.p1Var.get() == True:
            try:
                m1money = int(self.m1Box.get())
            except ValueError:
                m1money = 0
            
            if m1money > 0:
                if self.p1.balance < m1money: return messagebox.showerror("error", "Insufficient balance: Player 1.", parent=self)
        
        if self.p2Var.get() == True:
            try:
                m2money = int(self.m2Box.get())
            except ValueError:
                m2money = 0
            
            if m2money > 0:
                if self.p2.balance < m2money: return messagebox.showerror("error", "Insufficient balance: Player 2.", parent=self)
        
        self.p1.adjustBalance(-m1money)
        self.p2.adjustBalance(-m2money)
        self.p1.adjustBalance(m2money)
        self.p2.adjustBalance(m1money)
        
        if not self.p1 == None:
            self.game.savePlayerInfo(self.p1)
        if not self.p2 == None:
            self.game.savePlayerInfo(self.p2)

        if not loc1 == "":
            self.game.saveLocationInfo(loc1)
        if not loc2 == "":
            self.game.saveLocationInfo(loc2)

        # clean up
        self.p1 = None
        self.p2 = None
        self.p1Var.set(False)
        self.p2Var.set(False)
        self.p1Box.set("")
        self.p2Box.set("")
        self.m1Box.delete(0, "end")
        self.m2Box.delete(0, "end")

        self.game.returnToMain()
    
    def savePlayerLists(self):
        self.p1Box["values"] = [el for el in self.game.players.keys()]
        self.p2Box["values"] = [el for el in self.game.players.keys()]
    
    def loadP1Locations(self, e):
        name = self.p1Box.get()

        if name == "": return messagebox.showerror("error", "Player 1 name empty.", parent=self)

        self.p1 = self.game.players[name]
        self.p1Loc["values"] = [el.name for el in self.game.locations.values() if el.ownerId == self.p1.id]

    def loadP2Locations(self, e):
        name = self.p2Box.get()

        if name == "": return messagebox.showerror("error", "Player 2 name empty.", parent=self)

        self.p2 = self.game.players[name]
        self.p2Loc["values"] = [el.name for el in self.game.locations.values() if el.ownerId == self.p2.id]