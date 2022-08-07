import tkinter as tk


class GameMenu(tk.Menu):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = container

        mGame = tk.Menu(self, tearoff=0)

        mGame.add_command(label="Add Player", command=self.openAddPlayerWindow)
        mGame.add_separator()
        mGame.add_command(label="Reset Game", command=self.controller.game.resetGameState)
        mGame.add_separator()
        mGame.add_command(label="End Game", command=self.controller.game.endGame)
        mGame.add_separator()
        mGame.add_command(label="Exit", command=self.controller.safeExit)

        mPlayer = tk.Menu(self, tearoff=0)
        mPlayer.add_command(label="Add discount", command=self.openAddDiscountWindow)
        mPlayer.add_command(label="Add rent split", command=self.openAddRentSplitWindow)

        mLocation = tk.Menu(self, tearoff=0)
        mLocation.add_command(label="Inspect", command=self.inspectLocation)
        mLocation.add_command(label="Build", command=self.buildLocation)
        mLocation.add_command(label="Bulldoze", command=self.bulldozeLocation)
        mLocation.add_command(label="Sell", command=self.sellLocation)
        mLocation.add_command(label="Trade", command=self.tradeLocation)
        mLocation.add_command(label="Mortgage", command=self.mortgageLocation)

        self.add_cascade(label="Game", menu=mGame)
        self.add_cascade(label="Player", menu=mPlayer)
        self.add_cascade(label="Location", menu=mLocation)
        self.add_command(label="Return to main", command=self.controller.game.returnToMain)

    def openAddPlayerWindow(self):
        self.controller.showModule(self.controller.addPlayerFrame)

    def openAddDiscountWindow(self):
        self.controller.addDiscountFrame.updateInfo()
        self.controller.showModule(self.controller.addDiscountFrame)

    def openAddRentSplitWindow(self):
        self.controller.addSplitFrame.updateInfo()
        self.controller.showModule(self.controller.addSplitFrame)

    def inspectLocation(self):
        self.controller.showModule(self.controller.locInspectFrame)
    
    def buildLocation(self):
        self.controller.buildFrame.refreshData()
        self.controller.showModule(self.controller.buildFrame)
    
    def sellLocation(self):
        self.controller.sellFrame.refreshData()
        self.controller.showModule(self.controller.sellFrame)
    
    def mortgageLocation(self):
        self.controller.mortgageFrame.refreshData()
        self.controller.showModule(self.controller.mortgageFrame)
    
    def tradeLocation(self):
        self.controller.showModule(self.controller.tradeLocFrame)
    
    def bulldozeLocation(self):
        self.controller.bulldozeLocationFrame.refreshData()
        self.controller.showModule(self.controller.bulldozeLocationFrame)
    