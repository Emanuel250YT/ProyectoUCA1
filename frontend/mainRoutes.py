from flask import Flask, render_template
from backend import *


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        data = {
            "products": getAllProducts(baseDatos),
            "products_count": len(getAllProducts(baseDatos))
        }
        return render_template("index.html", data=data)

    @app.route("/productos")
    def products():
        data = {
            "products": getAllProducts(baseDatos),
            "products_count": len(getAllProducts(baseDatos))
        }
        return render_template("productos.html", data=data)

    @app.route("/sucursales")
    def sucursales():
        data = {
            "products": getAllProducts(baseDatos),
            "products_count": len(getAllProducts(baseDatos))
        }
        return render_template("sucursales.html", data=data)

# Skibidi papu estuvo aqui
