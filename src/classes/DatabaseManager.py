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
                if (perID):
                    for product in tempList:
                        if (product["id"] in perID):
                            products.append(product)
                if (perName):
                    for product in tempList:
                        if (product["name"] in perName):
                            products.append(product)
                if (not perName and not perID):
                    product = tempList
                return product
        except:
            self.createDatabase(db)
            return self.GetItems(db, perID, perName)

    def createDatabase(self, name):
        fileDirection = f"{self.baseFolder}\\src\\database\\{str(name)}.json"
        if os.path.isfile(fileDirection):
            print(f"El archivo '{fileDirection}' ya existe.")
            return
        with open(fileDirection, 'w') as file:
            json.dump({}, file)
