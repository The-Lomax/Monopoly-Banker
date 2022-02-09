import json
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
        self.apiRef = 'https://3s9l7asy39.execute-api.ap-southeast-1.amazonaws.com/test/'
        self.apiKey = ""
        self.pCount = 0
        self.players = {}
        self.locations = {}
        self.houses = {}
        self.poi = {}
        
        with open("C:\\Users\\Chris\\Documents\\awsapikey.txt") as mf:
            self.apiKey += mf.read()
        
        self.head = {
            "x-api-key": self.apiKey
        }

        self.loadData()
    
    def loadData(self):
        self.loadPlayersFromWeb()
        # self.loadLocationsFromWeb()
        # self.loadHousesFromWeb()
        # self.loadPOIFromWeb()

    def addPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        self.players[pName] = Player(pId, pName, pBal, pBkrupt)
        self.pCount += 1

    def createPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        query = f"INSERT INTO players (id, name, balance, bankrupt) " \
                f"VALUES ({pId}, '{pName}', {pBal}, {pBkrupt})"
        self.dbExecute(query, False)

    def addLocation(self, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId) -> None:
        self.locations[name] = Location(lId, name, buyPrice, json.loads(rent), mortgage, buildPrice, buildings, json.loads(rentSplits), json.loads(rentDiscounts), status, ownerId)

    def addHouse(self, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.houses[name] = House(lId, name, buyPrice, json.loads(rent), mortgage, status, ownerId)

    def addPOI(self, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.poi[name] = POI(lId, name, buyPrice, json.loads(rent), mortgage, status, ownerId)

    def loadHousesFromWeb(self):
        query = "SELECT * FROM houses"
        data = self.dbExecute(query, True)
        self.updateHousesList(data)

    def updateHousesList(self, list):
        self.houses = {}
        for el in list:
            lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addHouse(lId, name, buyPrice, rent, mortgage, status, ownerId)

    def loadPOIFromWeb(self):
        query = "SELECT * FROM poi"
        data = self.dbExecute(query, True)
        self.updatePOIList(data)

    def updatePOIList(self, list):
        self.poi = {}
        for el in list:
            lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addPOI(lId, name, buyPrice, rent, mortgage, status, ownerId)
    
    def loadLocationsFromWeb(self):
        query = "SELECT * FROM locations"
        data = self.dbExecute(query, True)
        self.updateLocationsList(data)

    def updateLocationsList(self, list):
        self.locations = {}
        for el in list:
            lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId = el
            self.addLocation(lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId)
    
    def loadPlayersFromWeb(self):
        data = requests.request(
            "GET",
            self.buildAPIURL("players")
        )
        data = data.json()
        for el in data:
            self.addPlayer(int(el["pId"]["N"]), str(el["pName"]), bal, bkrpt)

    def updatePlayersList(self, list):
        self.players = {}
        self.pCount = 0
        for i in range(1, len(list)):
            pId, pName, pBal, pBkrpt = list[i]
            self.addPlayer(pId, pName, pBal, pBkrpt)
    
    def buildAPIURL(self, param):
        return "".join([self.apiRef, param, "/"])
    
    def deletePlayer(self, pId):
        data = requests.request(
            'DELETE', 
            "".join([self.buildAPIURL("players"), str(pId)]),
            headers=self.head
        )
        return data
    
    def center(self, container, *app_size: int):
        return f"{app_size[0]}x{app_size[1]}+" + \
               f"{container.winfo_screenwidth() // 2 - app_size[0] // 2}+" + \
               f"{container.winfo_screenheight() // 2 - app_size[1] // 2}"

    def resetGameState(self):
        if messagebox.askyesno("Warning", "This will reset the game to default settings. Are you sure?", parent=self.mainWindow):
            
            for el in locationsInfo.values():
                data = requests.request(
                    'PUT', 
                    self.apiRef,
                    headers=self.head,
                    json=el
                )
            
            for el in housesInfo.values():
                data = requests.request(
                    'PUT', 
                    'https://3s9l7asy39.execute-api.ap-southeast-1.amazonaws.com/test/locations',
                    headers=self.head,
                    json=el
                )

            for el in poiInfo.values():
                data = requests.request(
                    'PUT', 
                    'https://3s9l7asy39.execute-api.ap-southeast-1.amazonaws.com/test/locations',
                    headers=self.head,
                    json=el
                )
            
            for el in self.players.values():
                self.deletePlayer(el['pId'])

            self.loadData()
            self.mainWindow.showModule(self.mainWindow.playersFrame)
            self.mainWindow.playersFrame.loadPlayers()
