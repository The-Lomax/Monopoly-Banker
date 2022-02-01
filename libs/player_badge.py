import tkinter as tk
from PIL import Image, ImageTk
from libs.add_money import AddMoney


class PlayerBadge(tk.Frame):
    def __init__(self, container, game, player, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.player = player
        self.game = game

        pad = 5
        btnSize = 30
        self.lFont = ("Helvetica", 24, "bold")

        # Images
        infoImg = Image.open("assets/info.png")
        scale = infoImg.resize((btnSize, btnSize))
        scaledInfoImg = ImageTk.PhotoImage(scale)

        addImg = Image.open("assets/add.png")
        scale = addImg.resize((btnSize, btnSize))
        scaledAddImg = ImageTk.PhotoImage(scale)

        # Labels
        self.pName = tk.Label(
            self,
            text=f"{self.player.name}",
            font=self.lFont
        )
        self.pName.pack(side="left", padx=(pad, 0))

        tk.Label(
            self,
            text=" - ",
            font=self.lFont
        ).pack(side="left", padx=(pad, 0))

        self.pBal = tk.Label(
            self,
            text=f"$ {int(self.player.balance)}",
            font=self.lFont
        )
        self.pBal.pack(side="left", padx=(pad, 0))

        # Buttons
        self.addBtn = tk.Button(
            self,
            command=self.addEvent
        )
        self.addBtn["image"] = scaledAddImg
        self.addBtn.image = scaledAddImg
        self.addBtn.pack(side="left", padx=(pad, 0))

    def addEvent(self):
        self.game.mainWindow.addEvent(self.player)
