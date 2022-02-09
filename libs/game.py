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
        self.loadLocationsFromWeb()
        self.loadHousesFromWeb()
        self.loadPOIFromWeb()

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

    def addLocation(self, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId) -> None:
        self.locations[name] = Location(lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId)

    def addHouse(self, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.houses[name] = House(lId, name, buyPrice, rent, mortgage, status, ownerId)

    def addPOI(self, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.poi[name] = POI(lId, name, buyPrice, rent, mortgage, status, ownerId)

    def loadHousesFromWeb(self):
        housesList = []
        data = requests.request(
            "GET",
            "".join([self.apiRef, "locations?loctype=house"])
        )
        data = data.json()
        for el in data:
            housesList.append([
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
            lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addHouse(lId, name, buyPrice, rent, mortgage, status, ownerId)

    def loadPOIFromWeb(self):
        poiList = []
        data = requests.request(
            "GET",
            "".join([self.apiRef, "locations?loctype=poi"])
        )
        data = data.json()
        for el in data:
            poiList.append([
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
            lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addPOI(lId, name, buyPrice, rent, mortgage, status, ownerId)
    
    def loadLocationsFromWeb(self):
        locationsList = []
        data = requests.request(
            "GET",
            "".join([self.apiRef, "locations?loctype=location"])
        )
        data = data.json()
        for el in data:
            rs = ''
            if el["lRentSplits"]["S"] == '':
                rs = {}
            else:
                rs = el["lRentSplits"]["S"]
            rd = ''
            if el["lRentDiscounts"]["S"] == '':
                rd = {}
            else:
                rd = el["lRentDiscounts"]["S"]
            locationsList.append([
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
            lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId = el
            self.addLocation(lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId)
    
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
        return "".join([self.apiRef, param, "/"])
    
    def deletePlayer(self, pId):
        requests.request(
            'DELETE', 
            "".join([self.buildAPIURL("players"), str(pId)]),
            headers=self.head
        )
    
    def center(self, container, *app_size: int):
        return f"{app_size[0]}x{app_size[1]}+" + \
               f"{container.winfo_screenwidth() // 2 - app_size[0] // 2}+" + \
               f"{container.winfo_screenheight() // 2 - app_size[1] // 2}"

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

            self.pCount = 0

            self.loadData()
            self.mainWindow.showModule(self.mainWindow.playersFrame)
            self.mainWindow.playersFrame.loadPlayers()
