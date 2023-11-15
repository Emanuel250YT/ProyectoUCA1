from flask import Flask, render_template, request, redirect, render_template_string
from backend import *
import pdfkit


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)
        return render_template("index.html", data=data, sucursales=sucursales)

    @app.route("/productos", methods=["GET", "POST"])
    def products():
        porID = request.args.get("id")
        porNombre = request.args.get("name")
        data = obtenerInformacionProductos(porID, porNombre)
        sucursales = obtenerInformacionSucursales(None)
        if (request.form):
            newID = int(max(data["products"], key=lambda x: x['id'])["id"]) + 1
            crearProducto(nameDB=baseDatos, id=newID, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            return redirect("/producto/"+str(newID))
        return render_template("productos.html", data=data, sucursales=sucursales)

    @app.route("/producto/<id>", methods=["GET", "POST"])
    def product(id):
        product = obtenerProducto(baseDatos, id)
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)

        if (product == None):
            return redirect("/productos")
        if (request.form):
            borrarProducto(baseDatos, id)
            crearProducto(nameDB=baseDatos, id=id, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            product = obtenerProducto(baseDatos, id)

        return render_template("producto.html", product=product, data=data, sucursales=sucursales)

    @app.route("/producto_eliminar/<id>", methods=["GET"])
    def productDelete(id):
        product = obtenerProducto(baseDatos, id)
        data = obtenerInformacionProductos(None, None)
        if (product != None):
            borrarProducto(baseDatos, id)
            return redirect("/productos")

    @app.route("/sucursales", methods=["GET", "POST"])
    def sucursales():
        porID = request.args.get("id")
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(porID=porID)
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
        product = obtenerProducto("Sucursales", id)
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)

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

            product = obtenerProducto("Sucursales", id)

        return render_template("sucursal.html", sucursal=product, data=data, sucursales=sucursales)

    @app.route("/ventas")
    def ventas():
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)

        return render_template("ventas.html", data=data, sucursales=sucursales)

    @app.route("/venta/<id>")
    def venta(id):
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)

        with open("frontend/templates/factura.html", 'r', encoding='utf-8') as file:
            content = file.read()
            render = render_template_string(content)
            pdfkit.from_string(
                content, "frontend/static/facturas/factura-"+id+".pdf")

        return render_template("ventas.html", data=data, sucursales=sucursales)


def obtenerInformacionProductos(porID, porNombre):
    allProducts = None
    if (porID or porNombre):
        allProducts = obtenerVariosProductos(baseDatos, [porNombre, porID])
    else:
        allProducts = obtenerTodosLosProductos(baseDatos)
    data = {
        "products": allProducts,
        "products_count": len(allProducts),
        "no_stock": [producto for producto in allProducts if producto['stock'] <= 0],
        "no_stock_count": len([producto for producto in allProducts if producto['stock'] <= 0])
    }
    return data


def obtenerInformacionSucursales(porID):
    allProducts = None
    if (porID):
        allProducts = [sucursal for sucursal in obtenerTodosLosProductos(
            sucursales) if int(sucursal["id"]) == int(porID)]
    else:
        allProducts = obtenerTodosLosProductos(sucursales)
    data = {
        "sucursales": allProducts,
        "sucursales_count": len(allProducts),
        # "no_stock": [producto for producto in allProducts if producto['stock'] <= 0],
        # "no_stock_count": len([producto for producto in allProducts if producto['stock'] <= 0])
    }
    return data

# Skibidi papu estuvo aqui
