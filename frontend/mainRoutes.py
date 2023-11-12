from flask import Flask, render_template


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        return render_template("index.html")

# Skibidi papu estuvo aqui
