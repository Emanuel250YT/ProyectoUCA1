''' Archivo main para gestión de productos '''
import json
import os


def crearBaseDeDatos(nombre):
    ''' Crea una nueva base de datos .JSON '''
    direccion_archivo = str(nombre) + ".json"
    if os.path.isfile(direccion_archivo):
        print(f"El archivo '{direccion_archivo}' ya existe.")
        return
    with open(str(nombre)+".json", 'w') as archivo:
        json.dump({}, archivo)


def crearProducto(nombreDB, id, nombre, desc, price, descuento, stock, categ, costo):
    ''' Permite añadir un nuevo producto a la base de datos especificada'''
    data = {
        "id": int(id),
        "descripcion": desc,
        "precio": price,
        "descuento": descuento,
        "stock": stock,
        "categoria": categ,
        "nombre": nombre,
        "costo": costo
    }

    try:
        with open(str(nombreDB) + ".json", 'r') as archivo:
            a = json.load(archivo)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        a = {}

    if id in a:
        return None

    a[id] = data

    with open(str(nombreDB) + ".json", 'w') as archivo2:
        json.dump(a, archivo2, indent=4)


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


def obtenerVariosProductos(db, productos):
    ''' Permite buscar varios productos pasandole un array de sus nombres'''
    with open(str(db)+".json", 'r') as archivo:
        load = json.load(archivo)
        listaProductos = []
        for product in productos:
            for productDB in load:
                tempProduct = load[productDB]
                if (str(tempProduct["id"]) == str(product)):
                    listaProductos.append(tempProduct)
                elif (tempProduct["nombre"] == product):
                    listaProductos.append(tempProduct)

        return listaProductos


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
