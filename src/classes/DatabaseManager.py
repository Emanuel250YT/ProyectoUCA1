import json
import os
import copy
import random


class DatabaseManager:
    def __init__(self, baseFolder):
        self.baseFolder = baseFolder

    def GetItems(self, db, perID, perName):
        try:
            with open(f"{self.baseFolder}\\src\\database\\{str(db)}.json", 'r') as file:
                tempList = json.load(file)
                products = []
                parsedIDs = []
                parsedNames = []

                if (perID != None):
                    for i in range(0, len(perID)):
                        id = perID[i]
                        if (id != None and len(id) > 0):
                            parsedIDs.append(int(id))
                    # for id in perID:
                    #     if (id != None and len(id) > 0):
                    #         parsedIDs.append(int(id))

                if (perName != None):
                    for i in range(0, len(perName)):
                        id = perID[i]
                        if (id != None and len(id) > 0):
                            parsedNames.append(id)
                    # for id in perID:
                    #     if (id != None and len(id) > 0):
                    #         parsedNames.append(id)

                if (len(parsedIDs) > 0):

                    for id in parsedIDs:
                        for product in tempList:
                            if (tempList[product]["id"] == id):
                                element = copy.deepcopy(tempList[product])
                                element["randomUUID"] = random.randint(
                                    0, 1_000_000_000)
                                products.append(element)
                    # for product in tempList:
                    #     if (tempList[product]["id"] in parsedIDs):
                    #         element = copy.deepcopy(tempList[product])
                    #         element["randomUUID"] = random.randint(
                    #             0, 1_000_000_000)
                    #         products.append(element)
                elif (len(parsedNames) > 0):
                    for name in parsedNames:
                        for product in tempList:
                            if (tempList[product]["name"] == name):
                                element = copy.deepcopy(tempList[product])
                                element["randomUUID"] = random.randint(
                                    0, 1_000_000_000)
                                products.append(element)
                    # for product in tempList:
                    #     if (tempList[product]["name"] in parsedNames):
                    #         element = copy.deepcopy(tempList[product])
                    #         element["randomUUID"] = random.randint(
                    #             0, 1_000_000_000)
                    #         products.append(element)
                else:
                    products = tempList
                return products
        except:
            self.CreateDatabase(db)
            return self.GetItems(db, perID, perName)

    def CreateProduct(self, id, name, description, price, discount, stock, category, cost):

        fileDirection = f"{self.baseFolder}\\src\\database\\products.json"

        data = {
            "id": int(id),
            "description": description,
            "price": price,
            "discount": discount,
            "stock": stock,
            "category": category,
            "name": name,
            "cost": cost
        }

        try:
            with open(fileDirection, 'r') as file:
                a = json.load(file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            a = {}

        if id in a:
            return None

        a[id] = data

        with open(fileDirection, 'w') as file:
            json.dump(a, file, indent=4)

    def CreateDatabase(self, name):
        fileDirection = f"{self.baseFolder}\\src\\database\\{str(name)}.json"
        if os.path.isfile(fileDirection):
            print(f"El archivo '{fileDirection}' ya existe.")
            return
        with open(fileDirection, 'w') as file:
            json.dump({}, file)

    def GetItem(self, db, id):
        with open(f"{self.baseFolder}\\src\\database\\{str(db)}.json", 'r') as file:
            load = json.load(file)
            try:
                if (load[id]):
                    return load[id]
            except:
                return None

    def DeleteItem(self, db, id):
        with open(f"{self.baseFolder}\\src\\database\\{str(db)}.json", "r+") as file:
            load = json.load(file)
        try:
            load.pop(id)

            with open(f"{self.baseFolder}\\src\\database\\{str(db)}.json", 'w') as file:
                json.dump(load, file, indent=4)
        except KeyError:
            print("No existe tal elemento!")

    def CreateBranch(self, id, details):

        fileDirection = f"{self.baseFolder}\\src\\database\\branchs.json"

        try:
            with open(fileDirection, 'r') as archivo:
                load = json.load(archivo)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            load = {}

        if str(id) in load:
            return None
        data = details
        data["id"] = id

        load[str(id)] = data
        with open(fileDirection, 'w') as archivo2:
            json.dump(load, archivo2, indent=4)

    def CreateSale(self, id, details):

        fileDirection = f"{self.baseFolder}\\src\\database\\sales.json"

        try:
            with open(fileDirection, 'r') as archivo:
                load = json.load(archivo)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            load = {}

        if str(id) in load:
            return None
        data = details
        data["id"] = id

        load[str(id)] = data
        with open(fileDirection, 'w') as archivo2:
            json.dump(load, archivo2, indent=4)
