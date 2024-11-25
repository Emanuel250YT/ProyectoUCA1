import os
import json
from flask import Flask, render_template, request, redirect, render_template_string, send_from_directory, send_file
import pdfkit
from datetime import datetime

from src.classes import DatabaseManager, InformationManager


class RouterHandlerManager():
    def __init__(self, baseFolder):
        self.app = Flask(
            "Server", template_folder=baseFolder+"\\src\\templates", static_folder=baseFolder+"\\src\\static")
        self.informationManager = InformationManager.InformationManager(
            baseFolder)
        self.setMainRoutes(self.app)

        print("created Server")

    def setMainRoutes(self, app):
        @app.route("/")
        def index():
            products = self.informationManager.GetProductsInfo(None, None)
            branchs = self.informationManager.GetBranchsInfo(None)
            sales = self.informationManager.GetSalesInfo(None)

            return render_template("index.html", products=products, branchs=branchs, sales=sales)

        @app.route("/productos", methods=["GET", "POST"])
        def products():
            perID = request.args.get("id")
            perName = request.args.get("name")
            products = self.informationManager.GetProductsInfo([perID], [
                                                               perName])
            branchs = self.informationManager.GetBranchsInfo(None)
            sales = self.informationManager.GetSalesInfo(None)

            if (request.form):

                newID = len(products["products"])

                if (len(products["products"]) > 0):
                    maxVal = 0
                    for product in products["products"]:
                        if (maxVal < int(products["products"][product]["id"])):
                            maxVal = int(products["products"][product]["id"])
                            newID = maxVal+1

                name = request.form.get("name")
                description = request.form.get("description")
                price = int(request.form.get("price"))
                discount = int(request.form.get(
                    "discount"))
                category = request.form.get(
                    "category")
                stock = int(
                    request.form.get("stock"))
                cost = int(request.form.get("cost"))

                self.informationManager.CreateProduct(
                    newID, name, description, price, discount, category, stock, cost)

                return redirect("/producto/"+str(newID))

            return render_template("productos.html", products=products, branchs=branchs, sales=sales)

        @app.route("/producto/<id>", methods=["GET", "POST"])
        def product(id):
            product = self.informationManager.GetProduct(id)
            products = self.informationManager.GetProductsInfo(None, None)
            branchs = self.informationManager.GetBranchsInfo(None)
            sales = self.informationManager.GetSalesInfo(None)

            if (product == None):
                return redirect("/productos")
            if (request.form):

                name = request.form.get("name")
                description = request.form.get("description")
                price = int(request.form.get("price"))
                discount = int(request.form.get(
                    "discount"))
                category = request.form.get(
                    "category")
                stock = int(
                    request.form.get("stock"))
                cost = int(request.form.get("cost"))

                self.informationManager.DeleteProduct(id)

                self.informationManager.CreateProduct(
                    id, name, description, price, discount, category, stock, cost)

                product = self.informationManager.GetProduct(id)

            return render_template("producto.html", product=product, products=products, branchs=branchs, sales=sales)

        @app.route("/producto_eliminar/<id>", methods=["GET"])
        def productDelete(id):
            product = self.informationManager.GetProduct(id)
            if (product != None):
                self.informationManager.DeleteProduct(id)
                return redirect("/productos")

        @app.route("/sucursales", methods=["GET", "POST"])
        def sucursales():
            perID = request.args.get("id")
            products = self.informationManager.GetProductsInfo(None, None)
            branchs = self.informationManager.GetBranchsInfo([perID])
            sales = self.informationManager.GetSalesInfo(None)

            if (request.form):

                newID = len(branchs["branchs"])

                if (len(branchs["branchs"]) > 0):
                    maxVal = 0
                    for branch in branchs["products"]:
                        if (maxVal < int(branchs["branchs"][branch]["id"])):
                            maxVal = int(branchs["branchs"][branch]["id"])
                            newID = maxVal+1

                self.informationManager.CreateBranch(id=newID, details={
                    "id": newID,
                    "products": request.form.get("products").split(" "),
                    "description": request.form.get("description"),
                    "name": request.form.get("name")
                })

                return redirect("/sucursal/"+str(newID))

            return render_template("sucursales.html", products=products, branchs=branchs, sales=sales)

        @app.route("/sucursal/<id>", methods=["GET", "POST"])
        def sucursal(id):
            currentBranch = self.informationManager.GetBranch(id)
            products = self.informationManager.GetProductsInfo(None, None)
            branchs = self.informationManager.GetBranchsInfo(None)
            sales = self.informationManager.GetSalesInfo(None)

            if (product == None):
                return redirect("/productos")
            if (request.form):

                self.informationManager.DeleteBranch(id)
                self.informationManager.CreateBranch(id, details={
                    "id": id,
                    "products": request.form.get("products").split(" "),
                    "description": request.form.get("description"),
                    "name": request.form.get("name")
                })

                currentBranch = self.informationManager.GetBranch(id)

            return render_template("sucursal.html", branch=currentBranch, products=products, branchs=branchs, sales=sales)

        @app.route("/sucursal_eliminar/<id>", methods=["GET"])
        def sucursalDelete(id):
            branch = self.informationManager.GetBranch(id)
            if (branch != None):
                self.informationManager.DeleteBranch(id)
                return redirect("/sucursales")

        # FIXED

        @app.route("/ventas", methods=["GET", "POST"])
        def ventas():
            products = self.informationManager.GetProductsInfo(None, None)
            branchs = self.informationManager.GetBranchsInfo(None)
            sales = self.informationManager.GetSalesInfo(None)

            if (request.form):
                newID = len(sales["sales"])

                if (len(sales["sales"]) > 0):
                    maxVal = 0
                    for sale in sales["sales"]:
                        if (maxVal < int(sales["sales"][sale]["id"])):
                            maxVal = int(sales["sales"][sale]["id"])
                            newID = maxVal+1

                productsWithoutType = request.form.get("products").split(" ")
                productsToRequest = []

                for product in productsWithoutType:
                    id = product.split(":")[0] or "0"
                    productsToRequest.append(id)

                productsInDB = self.informationManager.GetProductsInfo(productsToRequest, [
                    None])
                productsToSold = []

                for productContent in productsWithoutType:
                    id = productContent.split(":")[0] or "0"
                    amount = productContent.split(":")[1] or "0"
                    for product in productsInDB["products"]:
                        if (int(product["stock"]) >= int(amount) and int(product["id"]) == int(id)):
                            product["stock"] = int(
                                product["stock"]) - int(amount)
                            product["amount"] = int(amount)

                            self.informationManager.DeleteProduct(id)

                            self.informationManager.CreateProduct(
                                id, product["name"], product["description"], product["price"], product["discount"], product["category"],
                                product["stock"], product["cost"])

                            productsToSold.append(product)

                details = {
                    "id": newID,
                    "date": datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                    "client": request.form.get("client"),
                    "branch": request.form.get("branch"),
                    "products": productsToSold
                }

                self.informationManager.CreateSale(newID, details=details)

                return redirect("/ventas")
            return render_template("ventas.html", products=products, branchs=branchs, sales=sales)

        @app.route("/facturas/<id>")
        def facturas(id):

            data = obtenerInformacionProductos(None, None)
            sucursales = obtenerInformacionSucursales(None)
            ventas = obtenerInformacionVentas(id)
            venta = ventas["ventas"][0]

            with open("frontend/templates/factura.html", 'r', encoding='utf-8') as file:
                content = file.read()
                render = render_template_string(
                    content, data=data, sucursales=sucursales, venta=venta, total=sum(producto["precio"] for producto in venta["productos"]))
                pdfkit.from_string(
                    render, "frontend/static/facturas/factura-"+id+".pdf")
            return send_file(f"static/facturas/factura-{id}.pdf", as_attachment=True)

    def Start(self, port=80):
        self.app.run("127.0.0.1", port, debug=True)
