from flask import Flask, render_template, request
from backend import *


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        data = getData()
        return render_template("index.html", data=data)

    @app.route("/productos", methods=["GET", "POST"])
    def products():
        byId = request.args.get("id")
        byName = request.args.get("name")
        data = getData(byId, byName)
        return render_template("productos.html", data=data)

    @app.route("/sucursales")
    def sucursales():
        data = getData()
        return render_template("sucursales.html", data=data)


def getData(byId, byName):
    allProducts = None
    if (byId or byName):
        allProducts = getMultipleProducts(baseDatos, [byName, byId])
    else:
        allProducts = getAllProducts(baseDatos)
    data = {
        "products": allProducts,
        "products_count": len(allProducts),
        "no_stock": [producto for producto in allProducts if producto['stock'] <= 0],
        "no_stock_count": len([producto for producto in allProducts if producto['stock'] <= 0])
    }
    return data

# Skibidi papu estuvo aqui
