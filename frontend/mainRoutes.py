from flask import Flask, render_template, request, redirect, render_template_string, send_from_directory, send_file
from backend import *
import pdfkit
from datetime import datetime


def setMainRoutes(app=Flask):
    @app.route("/")
    def index():
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)
        ventas = obtenerInformacionVentas(None)
        return render_template("index.html", data=data, sucursales=sucursales, ventas=ventas)

    @app.route("/productos", methods=["GET", "POST"])
    def products():
        porID = request.args.get("id")
        porNombre = request.args.get("name")
        data = obtenerInformacionProductos(porID, porNombre)
        sucursales = obtenerInformacionSucursales(None)
        ventas = obtenerInformacionVentas(None)
        if (request.form):
            newID = int(max(data["products"], key=lambda x: x['id'])["id"]) + 1
            crearProducto(nombreDB=baseDatos, id=newID, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            return redirect("/producto/"+str(newID))
        return render_template("productos.html", data=data, sucursales=sucursales, ventas=ventas)

    @app.route("/producto/<id>", methods=["GET", "POST"])
    def product(id):
        product = obtenerProducto(baseDatos, id)
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)
        ventas = obtenerInformacionVentas(None)

        if (product == None):
            return redirect("/productos")
        if (request.form):
            borrarProducto(baseDatos, id)
            crearProducto(nombreDB=baseDatos, id=id, name=request.form.get("nombre"), desc=request.form.get(
                "desc"), price=int(request.form.get("price")), descuento=int(request.form.get("descuento")), categ=request.form.get("categoria"), stock=int(request.form.get("stock")), costo=int(request.form.get("costo")))
            product = obtenerProducto(baseDatos, id)

        return render_template("producto.html", product=product, data=data, sucursales=sucursales, ventas=ventas)

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
            crearSucursal(nombreDB="Sucursales", id=newID, detalles={
                "id": newID,
                "productos": request.form.get("productos").split(" "),
                "description": request.form.get("desc"),
                "nombre": request.form.get("nombre")
            })
            return redirect("/sucursal/"+str(newID))
        return render_template("sucursales.html", data=data, sucursales=sucursales, ventas=ventas)

    @app.route("/sucursal/<id>", methods=["GET", "POST"])
    def sucursal(id):
        product = obtenerProducto("Sucursales", id)
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)
        ventas = obtenerInformacionVentas(None)

        if (product == None):
            return redirect("/productos")
        if (request.form):
            eliminarSucursal("Sucursales", id)
            crearSucursal(nombreDB="Sucursales", id=id, detalles={
                "id": id,
                "productos": request.form.get("productos").split(" "),
                "description": request.form.get("desc"),
                "nombre": request.form.get("nombre")
            })

            product = obtenerProducto("Sucursales", id)

        return render_template("sucursal.html", sucursal=product, data=data, sucursales=sucursales, ventas=ventas)

    @app.route("/sucursal_eliminar/<id>", methods=["GET"])
    def sucursalDelete(id):
        product = obtenerProducto("Sucursales", id)
        data = obtenerInformacionSucursales(None)
        if (product != None):
            eliminarSucursal("Sucursales", id)
            return redirect("/sucursales")

    @app.route("/ventas", methods=["GET", "POST"])
    def ventas():
        porID = request.args.get("id")
        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)
        ventas = obtenerInformacionVentas(None)
        v = obtenerInformacionVentas(porID)

        productosVendidos = []
        sucursalObjetivo = obtenerInformacionSucursales(
            request.form.get("sucursal"))["sucursales"][0]
        if (request.form):
            newID = 0
            if (v["ventas_count"] > 0):
                newID = int(max(v["ventas"],
                                key=lambda x: x['id'])["id"]) + 1
            crearSucursal("Ventas", newID, detalles={
                "id": newID,
                "fecha": datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                "beneficiario": request.form.get("beneficiario"),
                "sucursal": sucursalObjetivo,
                "productos": obtenerVariosProductos("BaseDatos", request.form.get("productos").split(" "))
            })
            # return redirect("/venta/"+str(newID))
        return render_template("ventas.html", data=data, sucursales=sucursales, ventas=ventas)

    @app.route("/facturas/<id>")
    def facturas(id):

        data = obtenerInformacionProductos(None, None)
        sucursales = obtenerInformacionSucursales(None)
        ventas = obtenerInformacionVentas(id)
        venta = ventas["ventas"][0]


        with open("frontend/templates/factura.html", 'r', encoding='utf-8') as file:
            content = file.read()
            render = render_template_string(
                content, data=data, sucursales=sucursales, venta=venta, total= sum(producto["precio"] for producto in venta["productos"]))
            pdfkit.from_string(
                render, "frontend/static/facturas/factura-"+id+".pdf")
        return send_file(f"static/facturas/factura-{id}.pdf", as_attachment=True)


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
    }
    return data


def obtenerInformacionVentas(porID):
    allProducts = None
    if (porID):
        allProducts = [sucursal for sucursal in obtenerTodosLosProductos(
            "Ventas") if int(sucursal["id"]) == int(porID)]
    else:
        allProducts = obtenerTodosLosProductos("Ventas")
    data = {
        "ventas": allProducts,
        "ventas_count": len(allProducts),
    }
    return data

# Skibidi papu estuvo aqui
