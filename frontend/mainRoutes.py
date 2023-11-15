from flask import Flask, render_template, request, redirect, render_template_string
from backend import *
import pdfkit


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        data = getData(None, None)
        sucursales = getDataSucursales(None)
        return render_template("index.html", data=data, sucursales=sucursales)

    @app.route("/productos", methods=["GET", "POST"])
    def products():
        byId = request.args.get("id")
        byName = request.args.get("name")
        data = getData(byId, byName)
        sucursales = getDataSucursales(None)
        if (request.form):
            newID = int(max(data["products"], key=lambda x: x['id'])["id"]) + 1
            addProduct(nameDB=baseDatos, id=newID, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            return redirect("/producto/"+str(newID))
        return render_template("productos.html", data=data, sucursales=sucursales)

    @app.route("/producto/<id>", methods=["GET", "POST"])
    def product(id):
        product = getProduct(baseDatos, id)
        data = getData(None, None)
        sucursales = getDataSucursales(None)

        if (product == None):
            return redirect("/productos")
        if (request.form):
            deleteProduct(baseDatos, id)
            addProduct(nameDB=baseDatos, id=id, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            product = getProduct(baseDatos, id)

        return render_template("producto.html", product=product, data=data, sucursales=sucursales)

    @app.route("/producto_eliminar/<id>", methods=["GET"])
    def productDelete(id):
        product = getProduct(baseDatos, id)
        data = getData(None, None)
        if (product != None):
            deleteProduct(baseDatos, id)
            return redirect("/productos")

    @app.route("/sucursales", methods=["GET", "POST"])
    def sucursales():
        byId = request.args.get("id")
        data = getData(None, None)
        sucursales = getDataSucursales(byId=byId)
        if (request.form):
            newID = int(max(sucursales["sucursales"],
                        key=lambda x: x['id'])["id"]) + 1
            crearSucursal(nameDB="Sucursales", id=newID, detalles={
                "id": newID,
                "productos": request.form.get("productos").split(" "),
                "description": request.form.get("desc"),
                "nombre": request.form.get("nombre")
            })
            return redirect("/sucursal/"+str(newID))
        return render_template("sucursales.html", data=data, sucursales=sucursales)

    @app.route("/sucursal/<id>", methods=["GET", "POST"])
    def sucursal(id):
        product = getProduct("Sucursales", id)
        data = getData(None, None)
        sucursales = getDataSucursales(None)

        if (product == None):
            return redirect("/productos")
        if (request.form):
            eliminarSucursal("Sucursales", id)
            crearSucursal(nameDB="Sucursales", id=id, detalles={
                "id": id,
                "productos": request.form.get("productos").split(" "),
                "description": request.form.get("desc"),
                "nombre": request.form.get("nombre")
            })
            
            product = getProduct("Sucursales", id)

        return render_template("sucursal.html", sucursal=product, data=data, sucursales=sucursales)

    @app.route("/ventas")
    def ventas():
        data = getData(None, None)
        sucursales = getDataSucursales(None)

        return render_template("ventas.html", data=data, sucursales=sucursales)

    @app.route("/venta/<id>")
    def venta(id):
        data = getData(None, None)
        sucursales = getDataSucursales(None)

        with open("frontend/templates/factura.html", 'r', encoding='utf-8') as file:
            content = file.read()
            render = render_template_string(content)
            pdfkit.from_string(
                content, "frontend/static/facturas/factura-"+id+".pdf")

        return render_template("ventas.html", data=data, sucursales=sucursales)


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


def getDataSucursales(byId):
    allProducts = None
    if (byId):
        allProducts = [sucursal for sucursal in getAllProducts(
            sucursales) if int(sucursal["id"]) == int(byId)]
    else:
        allProducts = getAllProducts(sucursales)
    data = {
        "sucursales": allProducts,
        "sucursales_count": len(allProducts),
        # "no_stock": [producto for producto in allProducts if producto['stock'] <= 0],
        # "no_stock_count": len([producto for producto in allProducts if producto['stock'] <= 0])
    }
    return data

# Skibidi papu estuvo aqui
