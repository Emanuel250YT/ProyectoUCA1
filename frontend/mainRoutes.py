from flask import Flask, render_template, request, redirect
from backend import *
from operator import itemgetter, attrgetter


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
        if (request.form):
            newID = int(max(data["products"], key=lambda x: x['id'])["id"]) + 1
            addProduct(nameDB=baseDatos, id=newID, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            return redirect("/producto/"+str(newID))
        return render_template("productos.html", data=data)

    @app.route("/producto/<id>", methods=["GET", "POST"])
    def product(id):
        product = getProduct(baseDatos, id)
        data = getData(None, None)
        if (product == None):
            return redirect("/productos")
        if (request.form):
            deleteProduct(baseDatos, id)
            addProduct(nameDB=baseDatos, id=id, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            product = getProduct(baseDatos, id)

        return render_template("producto.html", product=product, data=data)

    @app.route("/producto_eliminar/<id>", methods=["GET"])
    def productDelete(id):
        product = getProduct(baseDatos, id)
        data = getData(None, None)
        if (product != None):
            deleteProduct(baseDatos, id)
            return redirect("/productos")

    @app.route("/sucursales")
    def sucursales():
        data = getData(None, None)
        return render_template("sucursales.html", data=data)
    
    @app.route("/ventas")
    def ventas():
        data = getData(None, None)
        return render_template("ventas.html", data=data)


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
