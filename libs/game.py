import math
import requests
from tkinter import messagebox
from libs.gameData import housesInfo, locationsInfo, poiInfo
from libs.house import House
from libs.location import Location
from libs.player import Player
from libs.poi import POI


class Game:
    def __init__(self):
        self.mainWindow = None
        self.apiRef = 'https://3s9l7asy39.execute-api.ap-southeast-1.amazonaws.com/test'
        self.apiKey = ""
        self.pCount = 0
        self.players = {}
        self.locations = {}
        self.houses = {}
        self.poi = {}
        
        with open("D:\\Documents\\awsapikey.txt") as mf:
            self.apiKey += mf.read()
        
        self.head = {
            "x-api-key": self.apiKey
        }

        self.loadData()

    def loadData(self):
        self.loadPlayersFromWeb()
        self.loadLocationsFromWeb()
        self.loadHousesFromWeb()
        self.loadPOIFromWeb()
    
    def endGame(self):
        # calculate net worth
        nets = {}
        for el in self.players.values():
            nets[el.id] = 0

        for el in self.locations.values():
            if el.status == "active":
                nets[el.ownerId] += el.buyPrice
            elif el.status == "mortgaged":
                nets[el.ownerId] += el.buyPrice - el.mortgage
            if el.buildings > 0:
                nets[el.ownerId] += el.buildings * el.buildPrice
        
        for el in self.houses.values():
            if el.status == "active":
                nets[el.ownerId] += el.buyPrice
            elif el.status == "mortgaged":
                nets[el.ownerId] += el.buyPrice - el.mortgage
        
        for el in self.poi.values():
            if el.status == "active":
                nets[el.ownerId] += el.buyPrice
            elif el.status == "mortgaged":
                nets[el.ownerId] += el.buyPrice - el.mortgage
        
        myStr = f""

        for el in self.players.values():
            nets[el.id] += el.balance
            myStr += f"{el.name}: {nets[el.id]}\n"
        
        messagebox.showinfo(
            "FINISH",
            myStr,
            parent=self.mainWindow
        )

    def addPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        self.players[pName] = Player(pId, pName, pBal, pBkrupt)
        self.pCount += 1

    def createPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        requests.request(
            "PUT",
            self.buildAPIURL("players"),
            headers=self.head,
            json={
                "pType": "player",
                "pId": pId,
                "pName": pName,
                "pBalance": pBal,
                "pBankrupt": pBkrupt
            }
        )
    
    def savePlayerInfo(self, player):
        self.createPlayer(player.id, player.name, player.balance, player.bankrupt)
    
    def saveLocationInfo(self, location):
        if location.name in self.locations.keys():
            if location.discounts == {}:
                ds = ""
            else:
                ds = location.discounts
            if location.rentSplits == {}:
                rs = ""
            else:
                rs = location.rentSplits
            js = {
                "lType": location.type,
                "lId": location.id,
                "lName": location.name,
                "lBuyPrice": location.buyPrice,
                "lRent": location.rent,
                "lMortgage": location.mortgage,
                "lBuildPrice": location.buildPrice,
                "lBuildings": location.buildings,
                "lRentSplits": rs,
                "lRentDiscounts": ds,
                "lStatus": location.status,
                "lOwnerId": location.ownerId
            }
        else:
            js = {
                "lType": location.type,
                "lId": location.id,
                "lName": location.name,
                "lBuyPrice": location.buyPrice,
                "lRent": location.rent,
                "lMortgage": location.mortgage,
                "lStatus": location.status,
                "lOwnerId": location.ownerId
            }
        
        if js == "": return messagebox.showerror("error", "Could not parse the object.")

        requests.request(
            'PUT', 
            self.buildAPIURL("locations"),
            headers=self.head,
            json=js
        )
    
    def returnToMain(self):
        self.mainWindow.playersFrame.loadPlayers()
        self.mainWindow.showModule(self.mainWindow.playersFrame)

    def addLocation(self, lType, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId) -> None:
        self.locations[name] = Location(lType, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId)

    def addHouse(self, lType, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.houses[name] = House(lType, lId, name, buyPrice, rent, mortgage, status, ownerId)

    def addPOI(self, lType, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.poi[name] = POI(lType, lId, name, buyPrice, rent, mortgage, status, ownerId)

    def loadHousesFromWeb(self):
        housesList = []
        data = requests.request(
            "GET",
            self.buildAPIURL("locations?loctype=house")
        )
        data = data.json()
        for el in data:
            housesList.append([
                el["lType"]["S"],
                int(el["lId"]["N"]),
                str(el["lName"]["S"]),
                int(el["lBuyPrice"]["N"]),
                tuple(int(x["N"]) for x in el["lRent"]["L"]),
                int(el["lMortgage"]["N"]),
                str(el["lStatus"]["S"]),
                int(el["lOwnerId"]["N"])
            ])
        self.updateHousesList(housesList)

    def updateHousesList(self, list):
        self.houses = {}
        for el in list:
            lType, lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addHouse(lType, lId, name, buyPrice, rent, mortgage, status, ownerId)

    def loadPOIFromWeb(self):
        poiList = []
        data = requests.request(
            "GET",
            self.buildAPIURL("locations?loctype=poi")
        )
        data = data.json()
        for el in data:
            poiList.append([
                el["lType"]["S"],
                int(el["lId"]["N"]),
                str(el["lName"]["S"]),
                int(el["lBuyPrice"]["N"]),
                tuple(int(x["N"]) for x in el["lRent"]["L"]),
                int(el["lMortgage"]["N"]),
                str(el["lStatus"]["S"]),
                int(el["lOwnerId"]["N"])
            ])
        self.updatePOIList(poiList)

    def updatePOIList(self, list):
        self.poi = {}
        for el in list:
            lType, lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addPOI(lType, lId, name, buyPrice, rent, mortgage, status, ownerId)
    
    def loadLocationsFromWeb(self):
        locationsList = []
        data = requests.request(
            "GET",
            self.buildAPIURL("locations?loctype=location")
        )
        data = data.json()
        for el in data:
            rs = ''
            if "S" in el["lRentSplits"].keys():
                if el["lRentSplits"]["S"] == "":
                    rs = {}
                else:
                    rs = el["lRentSplits"]["S"]
            elif "M" in el["lRentSplits"].keys():
                rs = {}
                for key, itm in el["lRentSplits"]["M"].items():
                    rs[key] = int(itm["N"])

            rd = ''
            if "S" in el["lRentDiscounts"].keys():
                if el["lRentDiscounts"]["S"] == '':
                    rd = {}
                else:
                    rd = el["lRentDiscounts"]["S"]
            elif "M" in el["lRentDiscounts"].keys():
                rd = {}
                for key, itm in el["lRentDiscounts"]["M"].items():
                    rd[key] = int(itm["N"])
            
            locationsList.append([
                el["lType"]["S"],
                int(el["lId"]["N"]),
                str(el["lName"]["S"]),
                int(el["lBuyPrice"]["N"]),
                tuple(int(x["N"]) for x in el["lRent"]["L"]),
                int(el["lMortgage"]["N"]),
                int(el["lBuildPrice"]["N"]),
                int(el["lBuildings"]["N"]),
                rs, rd,
                str(el["lStatus"]["S"]),
                int(el["lOwnerId"]["N"])
            ])
        self.updateLocationsList(locationsList)

    def updateLocationsList(self, list):
        self.locations = {}
        for el in list:
            lType, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId = el
            self.addLocation(lType, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId)
    
    def loadPlayersFromWeb(self):
        playerList = []
        data = requests.request(
            "GET",
            self.buildAPIURL("players")
        )
        data = data.json()
        for el in data:
            playerList.append([int(el["pId"]["N"]), str(el["pName"]["S"]), int(el["pBalance"]["N"]), el["pBankrupt"]["BOOL"]])
        self.updatePlayersList(playerList)

    def updatePlayersList(self, list):
        self.players = {}
        self.pCount = 0
        for i in range(0, len(list)):
            pId, pName, pBal, pBkrpt = list[i]
            self.addPlayer(pId, pName, pBal, pBkrpt)
    
    def buildAPIURL(self, param):
        return "/".join([self.apiRef, param])
    
    def deletePlayer(self, pId):
        requests.request(
            'DELETE', 
            "/".join([self.buildAPIURL("players"), str(pId)]),
            headers=self.head
        )
    
    def updateStatus(self, msg):
        self.mainWindow.statusLabel.configure(text="status: " + msg)

    def resetGameState(self):
        if messagebox.askyesno("Warning", "This will reset the game to default settings. Are you sure?", parent=self.mainWindow):
            
            for el in locationsInfo.values():
                requests.request(
                    'PUT', 
                    self.buildAPIURL("locations"),
                    headers=self.head,
                    json=el
                )
            
            for el in housesInfo.values():
                requests.request(
                    'PUT', 
                    self.buildAPIURL("locations"),
                    headers=self.head,
                    json=el
                )

            for el in poiInfo.values():
                requests.request(
                    'PUT', 
                    self.buildAPIURL("locations"),
                    headers=self.head,
                    json=el
                )
            
            for el in self.players.values():
                self.deletePlayer(el.id)

            self.players = {}
            self.pCount = 0

            self.loadData()
            self.mainWindow.showModule(self.mainWindow.playersFrame)
            self.mainWindow.playersFrame.loadPlayers()
