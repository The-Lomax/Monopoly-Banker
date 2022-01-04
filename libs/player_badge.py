import tkinter as tk
from PIL import Image, ImageTk
from libs.player_info import PlayerInfo
from libs.add_money import AddMoney
from libs.take_money import TakeMoney


class PlayerBadge(tk.Frame):
    def __init__(self, container, player, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = container
        self.player = player

        pad = 5
        btnSize = 20
        self.lFont = ("Helvetica", 14)

        # Images
        infoImg = Image.open("assets/info.png")
        scale = infoImg.resize((btnSize, btnSize))
        scaledInfoImg = ImageTk.PhotoImage(scale)

        addImg = Image.open("assets/add.png")
        scale = addImg.resize((btnSize, btnSize))
        scaledAddImg = ImageTk.PhotoImage(scale)

        takeImg = Image.open("assets/take.png")
        scale = takeImg.resize((btnSize, btnSize))
        scaledTakeImg = ImageTk.PhotoImage(scale)

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
            text=f"$ {self.player.balance}",
            font=self.lFont
        )
        self.pBal.pack(side="left", padx=(pad, 0))

        # Buttons
        self.infoBtn = tk.Button(
            self,
            command=self.openInfo
        )
        self.infoBtn["image"] = scaledInfoImg
        self.infoBtn.image = scaledInfoImg
        self.infoBtn.pack(side="left", padx=(pad, 0))

        self.addBtn = tk.Button(
            self,
            command=self.addMoney
        )
        self.addBtn["image"] = scaledAddImg
        self.addBtn.image = scaledAddImg
        self.addBtn.pack(side="left", padx=(pad, 0))

        self.takeBtn = tk.Button(
            self,
            command=self.takeMoney
        )
        self.takeBtn["image"] = scaledTakeImg
        self.takeBtn.image = scaledTakeImg
        self.takeBtn.pack(side="left", padx=(pad, 0))

    def openInfo(self):
        PlayerInfo(self.player)

    def addMoney(self):
        AddMoney(self.controller, self.player)

    def takeMoney(self):
        TakeMoney(self.controller, self.player)
