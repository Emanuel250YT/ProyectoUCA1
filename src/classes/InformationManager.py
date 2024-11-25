from src.classes import DatabaseManager


class InformationManager:
    def __init__(self, baseFolder):

        self.baseFolder = baseFolder
        self.databaseManager = DatabaseManager.DatabaseManager(baseFolder)
        self.productsDB = "products"
        self.branchDB = "branchs"
        self.salesDB = "sales"
        print("created")

    def GetProductsInfo(self, perID, perName):
        allProducts = self.databaseManager.GetItems(
            self.productsDB, perID, perName)

        noStock = []

        for productID in allProducts:

            if (type(productID) is int or type(productID) is str):
                if (int(allProducts[str(productID)]["stock"]) <= 0):
                    noStock.append(allProducts[productID])
            else:
                if (int(productID["stock"]) <= 0):
                    noStock.append(allProducts[productID])

        data = {
            "products": allProducts,
            "products_count": len(allProducts),
            "no_stock": noStock,
            "no_stock_count": len(noStock)
        }
        return data

    def GetBranchsInfo(self, perID):
        allBranchs = self.databaseManager.GetItems(
            self.branchDB, perID, None)

        data = {
            "branchs": allBranchs,
            "branch_count": len(allBranchs),
        }
        return data

    def GetSalesInfo(self, perID):
        allSales = self.databaseManager.GetItems(self.salesDB, perID, None)

        totalCost = 0
        totalIncome = 0

        for sale in allSales:
            if (allSales[sale]["products"]):
                for product in allSales[sale]["products"]:
                    totalCost += int(product["cost"])
                    totalIncome += int(product["price"])

        data = {
            "sales": allSales,
            "sales_count": len(allSales),
            "total_income": totalIncome,
            "total_cost": totalCost
        }
        return data

    def CreateProduct(self, newID, name, description, price, discount, category, stock, cost):
        self.databaseManager.CreateProduct(
            newID, name, description, price, discount, category, stock, cost)

    def CreateBranch(self, id, details):
        return self.databaseManager.CreateBranch(id, details)

    def CreateSale(self, id, details):
        return self.databaseManager.CreateSale(id, details)

    def GetProduct(self, id):
        return self.databaseManager.GetItem(self.productsDB, id)

    def GetBranch(self, id):
        return self.databaseManager.GetItem(self.branchDB, id)

    def GetSale(self, id):
        return self.databaseManager.GetItem(self.salesDB, id)

    def DeleteProduct(self, id):
        return self.databaseManager.DeleteItem(self.productsDB, id)

    def DeleteBranch(self, id):
        return self.databaseManager.DeleteItem(self.branchDB, id)
