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
        self.databaseManager = DatabaseManager.DatabaseManager(baseFolder)
        self.setMainRoutes(self.app)

        print("created Server")

    def setMainRoutes(self, app):
        @app.route("/")
        def index():
            products = self.informationManager.GetProductsInfo(None, None)
            branchs = self.informationManager.GetBranchsInfo(None)
            sales = self.informationManager.GetSalesInfo(None)

            return render_template("index.html", products=products, branch=branchs, sales=sales)

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
                    newID = int(
                        max(products["products"], key=lambda x: x['id'])["id"]) + 1

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

                self.databaseManager.CreateProduct(
                    newID, name, description, price, discount, category, stock, cost)

                return redirect("/producto/"+str(newID))

            return render_template("productos.html", products=products, branchs=branchs, sales=sales)

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
            ventas = obtenerInformacionVentas(None)
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
                    content, data=data, sucursales=sucursales, venta=venta, total=sum(producto["precio"] for producto in venta["productos"]))
                pdfkit.from_string(
                    render, "frontend/static/facturas/factura-"+id+".pdf")
            return send_file(f"static/facturas/factura-{id}.pdf", as_attachment=True)

    def Start(self, port=80):
        self.app.run("127.0.0.1", port, debug=True)


def obtenerProducto(nombreDB, producto):
    ''' Permite obtener el diccionario del producto desde la BD'''
    with open(str(nombreDB)+".json", 'r') as archivo:
        load = json.load(archivo)
        try:
            if (load[producto]):
                return load[producto]
        except:
            return None


def borrarProducto(nombreDB, producto):
    ''' Permite eliminar un producto mediante su nombre '''
    with open(str(nombreDB)+".json", "r+") as archivo:
        load = json.load(archivo)
    try:
        load.pop(producto)

        with open(str(nombreDB)+".json", 'w') as archivo2:
            json.dump(load, archivo2, indent=4)
    except KeyError:
        print("No existe tal elemento!")


def borrarVariosProductos(nombreDB, productos):
    ''' Permite eliminar varios productos pasandole un array de sus nombres '''
    with open(str(nombreDB)+".json", "r+") as archivo:
        load = json.load(archivo)
    for producto in productos:
        try:
            load.pop(producto)
        except KeyError:
            print("No existe el elemento", producto)

    with open(str(nombreDB)+".json", 'w') as archivo2:
        json.dump(load, archivo2, indent=4)


def obtenerAtributo(db, nombreProducto, atributo):
    ''' Permite buscar atributos de un producto '''
    product = obtenerProducto(db, nombreProducto)
    if product == None:
        print("Ese producto no existe")
        return
    try:
        return product[atributo]
    except KeyError:
        print("El producto", nombreProducto, "no tiene", atributo)


def obtenerTodosLosProductos(db):
    ''' Devuelve todos los productos '''
    with open(str(db)+".json", 'r') as archivo:
        load = json.load(archivo)
        listaProductos = []
        for producto in load:
            listaProductos.append(load[producto])
        return listaProductos


def editarProducto(db, id, objeto):
    ''' Permite editar productos, pasandole la id y un Object con las propiedades a modificar'''
    with open(str(db)+".json", "r") as archivo:
        load = json.load(archivo)
    productoOriginal = load[id]
    try:
        for key in object:
            productoOriginal[key] = object[key]
        load[id] = productoOriginal
        with open(str(db)+".json", 'w') as archivo2:
            json.dump(load, archivo2, indent=4)
    except TypeError:
        print("Ese producto no existe!")


def crearSucursal(nombreDB, id, detalles):
    ''' Permite crear sucursales, pasandole una id y un object con los atributos que tendrá la sucursal'''
    try:
        with open(str(nombreDB) + ".json", 'r') as archivo:
            load = json.load(archivo)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        load = {}

    if str(id) in load:
        return None
    data = detalles
    data["id"] = id

    load[str(id)] = data
    with open(str(nombreDB) + ".json", 'w') as archivo2:
        json.dump(load, archivo2, indent=4)


def editarSucursal(nombreDB, id, detalles):
    ''' Permite editar una sucursal, pasandole la id y un object de los atributos a modificar'''
    id = str(id)
    try:
        with open(str(nombreDB) + ".json", 'r') as archivo:
            load = json.load(archivo)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("La base", nombreDB, "no existe.")
        return None
    if not (id in load):
        print("No se encontró el item con la id", id)
        return None
    for key in detalles:
        load[id][key] = detalles[key]

    with open(str(nombreDB) + ".json", 'w') as archivo2:
        json.dump(load, archivo2, indent=4)


def eliminarSucursal(nombreDB, id):
    ''' Permite eliminar una sucursal con su id '''
    id = str(id)
    try:
        with open(str(nombreDB) + ".json", 'r') as archivo:
            load = json.load(archivo)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("La base", nombreDB, "no existe.")
        return None
    if not (id in load):
        print("El producto", id, "no existe")
    load.pop(id)

    with open(str(nombreDB) + ".json", 'w') as archivo2:
        json.dump(load, archivo2, indent=4)


def obtenerProximaID(todasLasIDs):
    ''' Obtiene la proxima id disponible en una lista de ids, buscando si hay huecos'''
    try:
        nextID = min(set(range(1, max(todasLasIDs) + 2)) - todasLasIDs)
        return nextID
    except ValueError:
        return 0


def nuevaVenta(nombreDB, id, detalles):
    ''' Crea una nueva venta para la sucursal con la id propocionada '''
    id = str(id)
    with open(str(nombreDB) + ".json", 'r') as archivo:
        load = json.load(archivo)
    if not (id in load):
        print("No se encontró el item", id)
        return None
    if not ("ventas" in load[id]):  # Si no hay categoría ventas, crear una
        load[id]["ventas"] = {}
    # Obtiene la proxima ID disponible
    nextID = obtenerProximaID(set(map(int, load[id]["ventas"].keys())))
    detalles["id"] = nextID
    load[id]["ventas"][str(nextID)] = detalles
    with open(str(nombreDB) + ".json", 'w') as archivo2:
        json.dump(load, archivo2, indent=4)


def buscarVenta(nombreDB, sucursal, id):
    ''' Permite buscar una venta por su id '''
    sucursal = str(sucursal)
    id = str(id)
    with open(str(nombreDB) + ".json", 'r') as archivo:
        load = json.load(archivo)

    if not (sucursal in load):
        print("No existe esa sucursal!")
        return None
    if not (load[sucursal]["ventas"]):
        print("Esa sucursal no tiene ventas!")
        return None
    if not (id in load[sucursal]["ventas"]):
        print("Esa venta no existe!")
        return None

    return load[sucursal]["ventas"][id]


baseDatos = "BaseDatos"
sucursales = "Sucursales"
