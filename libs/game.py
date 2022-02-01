import sqlite3
import json
import os
from tkinter import messagebox
from libs.player import Player
from libs.location import Location
from libs.house import House
from libs.poi import POI
from libs.gameData import locationsInfo, housesInfo, poiInfo


class Game:
    def __init__(self):
        self.dbFile = "assets/game.sqlite"
        self.mainWindow = None
        self.pCount = 0
        self.players = {}
        self.locations = {}
        self.houses = {}
        self.poi = {}

        # Check if database exists and create if does not exist
        if not os.path.isfile(self.dbFile):
            self.buildDb()
        else:  # Database exists, proceed to load game data
            self.loadData()

    def addPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        self.players[pName] = Player(pId, pName, pBal, pBkrupt)
        self.pCount += 1

    def createPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        query = f"INSERT INTO players (id, name, balance, bankrupt) " \
                f"VALUES ({pId}, '{pName}', {pBal}, {pBkrupt})"
        self.dbExecute(query, False)

    def loadData(self):
        self.loadPlayersFromDB()
        self.loadLocationsFromDB()
        self.loadHousesFromDB()
        self.loadPOIFromDB()

    def addLocation(self, lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId) -> None:
        self.locations[name] = Location(lId, name, buyPrice, json.loads(rent), mortgage, buildPrice, buildings, json.loads(rentSplits), json.loads(rentDiscounts), status, ownerId)

    def addHouse(self, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.houses[name] = House(lId, name, buyPrice, json.loads(rent), mortgage, status, ownerId)

    def addPOI(self, lId, name, buyPrice, rent, mortgage, status, ownerId):
        self.poi[name] = POI(lId, name, buyPrice, json.loads(rent), mortgage, status, ownerId)

    def loadHousesFromDB(self):
        query = "SELECT * FROM houses"
        data = self.dbExecute(query, True)
        self.updateHousesList(data)

    def updateHousesList(self, list):
        self.houses = {}
        for el in list:
            lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addHouse(lId, name, buyPrice, rent, mortgage, status, ownerId)

    def loadPOIFromDB(self):
        query = "SELECT * FROM poi"
        data = self.dbExecute(query, True)
        self.updatePOIList(data)

    def updatePOIList(self, list):
        self.poi = {}
        for el in list:
            lId, name, buyPrice, rent, mortgage, status, ownerId = el
            self.addPOI(lId, name, buyPrice, rent, mortgage, status, ownerId)
    
    def loadLocationsFromDB(self):
        query = "SELECT * FROM locations"
        data = self.dbExecute(query, True)
        self.updateLocationsList(data)

    def updateLocationsList(self, list):
        self.locations = {}
        for el in list:
            lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId = el
            self.addLocation(lId, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId)
    
    def loadPlayersFromDB(self):
        query = "SELECT * FROM players"
        data = self.dbExecute(query, True)
        self.updatePlayersList(data)

    def updatePlayersList(self, list):
        self.players = {}
        self.pCount = 0
        for i in range(1, len(list)):
            pId, pName, pBal, pBkrpt = list[i]
            self.addPlayer(pId, pName, pBal, pBkrpt)
    
    def center(self, container, *app_size: int):
        return f"{app_size[0]}x{app_size[1]}+" + \
               f"{container.winfo_screenwidth() // 2 - app_size[0] // 2}+" + \
               f"{container.winfo_screenheight() // 2 - app_size[1] // 2}"

    def resetGameState(self):
        if messagebox.askyesno("Warning", "This will reset the game to default settings. Are you sure?", parent=self.mainWindow):
            db = sqlite3.connect(self.dbFile)
            cursor = db.cursor()

            query = f"DELETE FROM players WHERE id>0"
            cursor.execute(query)

            query = f"UPDATE houses SET status='free', ownerId=0"
            cursor.execute(query)

            query = f"UPDATE poi SET status='free', ownerId=0"
            cursor.execute(query)

            query = f"UPDATE locations SET buildings=0, rentSplits='{json.dumps(dict())}', rentDiscounts='{json.dumps(dict())}', status='free', ownerId=0"
            cursor.execute(query)

            db.commit()
            db.close()

            self.loadData()
            self.mainWindow.showModule(self.mainWindow.playersFrame)
            self.mainWindow.playersFrame.loadPlayers()

    def buildDb(self):
        db = sqlite3.connect(self.dbFile)
        cursor = db.cursor()

        query = f"CREATE TABLE IF NOT EXISTS players (" \
                f"id INTEGER, " \
                f"name TEXT, " \
                f"balance INTEGER, " \
                f"bankrupt INTEGER);"
        cursor.execute(query)

        query = f"INSERT INTO players (id, name, balance, bankrupt) " \
                f"VALUES (0, 'Bank', 0, 0);"
        cursor.execute(query)

        query = f"CREATE TABLE IF NOT EXISTS locations (" \
                f"id INTEGER, " \
                f"name TEXT, " \
                f"buyPrice INTEGER, " \
                f"rent TEXT, " \
                f"mortgage INTEGER, " \
                f"buildPrice INTEGER, " \
                f"buildings INTEGER, " \
                f"rentSplits TEXT, " \
                f"rentDiscounts TEXT, " \
                f"status TEXT, " \
                f"ownerId INTEGER);"
        cursor.execute(query)

        for loc in locationsInfo.values():
            query = f"INSERT INTO locations (id, name, buyPrice, rent, mortgage, buildPrice, buildings, rentSplits, rentDiscounts, status, ownerId" \
                    f") VALUES (" \
                    f"{loc['id']},'{loc['name']}',{loc['buyPrice']}, '{json.dumps(loc['rent'])}', {loc['mortgage']}, {loc['buildPrice']}, " \
                    f"{loc['buildings']}, '{json.dumps(loc['rentSplits'])}', '{json.dumps(loc['rentDiscounts'])}', '{loc['status']}', {loc['ownerId']});"
            cursor.execute(query)

        query = f"CREATE TABLE IF NOT EXISTS houses (" \
                f"id INTEGER NOT NULL, " \
                f"name TEXT, " \
                f"buyPrice INTEGER, " \
                f"rent TEXT, " \
                f"mortgage INTEGER, " \
                f"status TEXT, " \
                f"ownerId INTEGER);"
        cursor.execute(query)

        for house in housesInfo.values():
            query = f"INSERT INTO houses (" \
                    f"id, name, buyPrice, rent, mortgage, status, ownerId" \
                    f") VALUES (" \
                    f"{house['id']},'{house['name']}',{house['buyPrice']}, '{json.dumps(house['rent'])}', {house['mortgage']}, '{house['status']}', {house['ownerId']});"
            cursor.execute(query)

        query = f"CREATE TABLE IF NOT EXISTS poi (" \
                f"id INTEGER NOT NULL, " \
                f"name TEXT, " \
                f"buyPrice INTEGER, " \
                f"rent TEXT, " \
                f"mortgage INTEGER, " \
                f"status TEXT, " \
                f"ownerId INTEGER);"
        cursor.execute(query)

        for poi in poiInfo.values():
            query = f"INSERT INTO poi (" \
                    f"id, name, buyPrice, rent, mortgage, status, ownerId" \
                    f") VALUES (" \
                    f"{poi['id']},'{poi['name']}',{poi['buyPrice']}, '{json.dumps(poi['rent'])}', {poi['mortgage']}, '{poi['status']}', {poi['ownerId']});"
            cursor.execute(query)

        db.commit()
        db.close()

    def dbExecute(self, query: str, ret: bool) -> list or None:
        # Execute query
        db = sqlite3.connect(self.dbFile)
        cursor = db.cursor()
        cursor.execute(query)

        # Return data if required by user
        if ret:
            data = cursor.fetchall()

            # Save the database
            db.commit()

            # Close connection
            db.close()

            return data
        else:
            db.commit()
            db.close()
