from flask import Flask, render_template


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/productos")
    def products():
        return render_template("productos.html")
    
    @app.route("/sucursales")
    def sucursales():
        return render_template("sucursales.html")

# Skibidi papu estuvo aqui
