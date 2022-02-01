import sqlite3, json, os
from tkinter import messagebox
from libs.player import Player
from libs.location import Location
from libs.gameData import locationsInfo, housesInfo, poiInfo


class Game:
    def __init__(self):
        self.dbFile = "assets/game.sqlite"
        self.pCount = 0
        self.players = {}
        self.locations = {}

        # Check if database exists and create if does not exist
        if not os.path.isfile(self.dbFile):
            self.buildDb()
        else:  # Database exists, proceed to load game data
            self.loadData()

    def addPlayer(self, pId: int, pName: str, pBal: int, pBkrupt: bool) -> None:
        self.players[pName] = Player(pId, pName, pBal, pBkrupt)

    def addLocation(self, loc: str) -> None:
        self.locations[loc] = Location(loc)

    def loadData(self):
        self.loadPlayers()
        self.loadLocations()
    
    def loadLocations(self):
        query = "SELECT "
    
    def loadPlayers(self):
        query = "SELECT * FROM players"
        data = self.dbExecute(query, True)
        for i in range(1, len(data)):
            self.addPlayer(data[i][0], data[i][1], data[i][2], data[i][3])
            self.pCount += 1
    
    def center_app(self, container, *app_size: int):
        """
        used to center the position of opened windows. Returns formatted tkinter.geometry parameter

        :param container: screen reference to get size in pixels
        :param app_size: desired size of the window to create
        :return: string containing size and position of window to create
        """

        return f"{app_size[0]}x{app_size[1]}+" + \
               f"{container.winfo_screenwidth() // 2 - app_size[0] // 2}+" + \
               f"{container.winfo_screenheight() // 2 - app_size[1] // 2}"

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
