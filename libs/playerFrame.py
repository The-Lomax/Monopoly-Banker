import tkinter as tk
from libs.player_badge import PlayerBadge


class PlayerList(tk.Frame):
    """
    Class used to store current information on players and their balances
    """
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.game = game

        self.loadPlayers()

    def loadPlayers(self):
        # clear list
        for el in self.winfo_children():
            if el.winfo_class() == "Frame":
                el.destroy()

        # recreate player badges
        pad = 5
        for player in self.game.players.values():
            if not player.isBankrupt():
                PlayerBadge(self, self.game, player).pack(fill="x", expand=True, padx=pad, pady=(pad, 0))
