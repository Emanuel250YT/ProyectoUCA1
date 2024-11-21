from src.classes import DatabaseManager


class InformationManager:
    def __init__(self, baseFolder):

        self.baseFolder = baseFolder
        self.databaseManager = DatabaseManager.DatabaseManager(baseFolder)
        self.productsDB = "products"
        self.branchDB = "branch"
        self.salesDB = "sales"
        print("created")

    def GetProductsInfo(self, perID, perName):
        allProducts = self.databaseManager.GetItems(
            self.productsDB, perID, perName)

        data = {
            "products": allProducts,
            "products_count": len(allProducts),
            "no_stock": [product for product in allProducts if product['stock'] <= 0],
            "no_stock_count": len([product for product in allProducts if product['stock'] <= 0])
        }
        return data

    def GetBranchsInfo(self, perID):
        allBranchs = self.databaseManager.GetItems(
            self.branchDB, perID, None)

        data = {
            "brachs": allBranchs,
            "branch_count": len(allBranchs),
        }
        return data

    def GetSalesInfo(self, perID):
        allSales = self.databaseManager.GetItems(self.salesDB, perID, None)

        totalCost = 0
        totalIncome = 0

        for sale in allSales:
            totalCost += sum(v["cost"] for v in sale["products"])
            totalIncome += sum(v["price"] for v in sale["products"])

        data = {
            "sales": allSales,
            "sales_count": len(allSales),
            "total_income": totalIncome,
            "total_cost": totalCost
        }
        return data
