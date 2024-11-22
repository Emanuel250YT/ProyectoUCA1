import json
import os


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
                    for id in perID:
                        if (id != None and len(id) > 0):
                            parsedIDs.append(int(id))

                if (perName != None):
                    for id in perID:
                        if (id != None and len(id) > 0):
                            parsedNames.append(id)

                if (len(parsedIDs) > 0):
                    for product in tempList:
                        if (tempList[product]["id"] in parsedIDs):
                            products.append(tempList[product])
                elif (len(parsedNames) > 0):
                    for product in tempList:
                        if (tempList[product]["name"] in parsedNames):
                            products.append(tempList[product])
                else:
                    products = tempList
                print(products)
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
