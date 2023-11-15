''' Archivo main para gestión de productos '''
import json
import os


def createNewDB(name):
    ''' Crea una nueva base de datos .JSON '''
    file_path = str(name) + ".json"
    if os.path.isfile(file_path):
        print(f"El archivo '{file_path}' ya existe.")
        return
    with open(str(name)+".json", 'w') as file:
        json.dump({}, file)


def addProduct(nameDB, id, name, desc, price, descuento, stock, categ, costo):
    ''' Permite añadir un nuevo producto a la base de datos especificada'''
    data = {
        "id": int(id),
        "descripcion": desc,
        "precio": price,
        "descuento": descuento,
        "stock": stock,
        "categoria": categ,
        "nombre": name,
        "costo": costo
    }

    try:
        with open(str(nameDB) + ".json", 'r') as file:
            a = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        a = {}

    if id in a:
        return None

    a[id] = data

    with open(str(nameDB) + ".json", 'w') as file:
        json.dump(a, file, indent=4)


def getProduct(db, product):
    ''' Permite obtener el diccionario del producto desde la BD'''
    with open(str(db)+".json", 'r') as file:
        load = json.load(file)
        try:
            if (load[product]):
                return load[product]
        except:
            return None


def deleteProduct(db, product):
    ''' Permite eliminar un producto mediante su nombre '''
    with open(str(db)+".json", "r+") as file:
        load = json.load(file)
    try:
        load.pop(product)

        with open(str(db)+".json", 'w') as file2:
            json.dump(load, file2, indent=4)
    except KeyError:
        print("No existe tal elemento!")


def deleteMultipleProducts(db, products):
    ''' Permite eliminar varios productos pasandole un array de sus nombres '''
    with open(str(db)+".json", "r+") as file:
        load = json.load(file)
    for product in products:
        try:
            load.pop(product)
        except KeyError:
            print("No existe el elemento", product)

    with open(str(db)+".json", 'w') as file2:
        json.dump(load, file2, indent=4)


def getMultipleProducts(db, products):
    ''' Permite buscar varios productos pasandole un array de sus nombres'''
    with open(str(db)+".json", 'r') as file:
        load = json.load(file)
        productList = []
        for product in products:
            for productDB in load:
                tempProduct = load[productDB]
                tempProduct["nombre"] = productDB
                if (str(tempProduct["id"]) == str(product)):
                    productList.append(tempProduct)
                elif (tempProduct["nombre"] == product):
                    productList.append(tempProduct)

        return productList


def getAttribute(db, productName, attribute):
    ''' Permite buscar atributos de un producto '''
    product = getProduct(db, productName)
    if product == None:
        print("Ese producto no existe")
        return
    try:
        return product[attribute]
    except KeyError:
        print("El producto", productName, "no tiene", attribute)


def getAllProducts(db):
    ''' Devuelve todos los productos '''
    with open(str(db)+".json", 'r') as file:
        load = json.load(file)
        productList = []

        for product in load:
            productList.append(load[product])
        return productList

def editProduct(db, id, object):
    ''' Permite editar productos, pasandole la id y un Object con las propiedades a modificar'''
    with open(str(db)+".json", "r") as file:
        load = json.load(file)
    originalProduct = load[id]
    try:
        for key in object:
            originalProduct[key] = object[key]
        load[id] = originalProduct
        with open(str(db)+".json", 'w') as file2:
            json.dump(load, file2, indent=4)
    except TypeError:
        print("Ese producto no existe!")

def crearSucursal(nameDB, id, detalles):
    ''' Permite crear sucursales, pasandole una id y un object con los atributos que tendrá la sucursal'''
    try:
        with open(str(nameDB) + ".json", 'r') as file:
            load = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        load = {}
    
    if str(id) in load:
        return None
    data = detalles
    data["id"] = id

    load[str(id)] = data
    with open(str(nameDB) + ".json", 'w') as file2:
        json.dump(load, file2, indent=4)

def editarSucursal(nameDB, id, detalles):
    ''' Permite editar una sucursal, pasandole la id y un object de los atributos a modificar'''
    id = str(id)
    try:
        with open(str(nameDB) + ".json", 'r') as file:
            load = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("La base", nameDB, "no existe.")
        return None
    if not(id in load):
        print("No se encontró el item con la id", id)
        return None
    for key in detalles:
        load[id][key] = detalles[key]

    with open(str(nameDB) + ".json", 'w') as file2:
        json.dump(load, file2, indent=4)

def eliminarSucursal(nameDB, id):
    ''' Permite eliminar una sucursal con su id '''
    id = str(id)
    try:
        with open(str(nameDB) + ".json", 'r') as file:
            load = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("La base", nameDB, "no existe.")
        return None
    if not(id in load):
        print("El producto", id, "no existe")
    load.pop(id)

    with open(str(nameDB) + ".json", 'w') as file2:
        json.dump(load, file2, indent=4)


def getNextID(allIDs):
    ''' Obtiene la proxima id disponible en una lista de ids, buscando si hay huecos'''
    try:
        nextID = min(set(range(1, max(allIDs) + 2)) - allIDs)
        return nextID
    except ValueError:
        return 0

def nuevaVenta(nameDB, id, detalles):
    ''' Crea una nueva venta para la sucursal con la id propocionada '''
    id = str(id)
    with open(str(nameDB) + ".json", 'r') as file:
            load = json.load(file)
    if not(id in load):
        print("No se encontró el item", id)
        return None
    if not("ventas" in load[id]): # Si no hay categoría ventas, crear una
        load[id]["ventas"] = {}
    nextID = getNextID(set(map(int, load[id]["ventas"].keys()))) # Obtiene la proxima ID disponible
    detalles["id"] = nextID
    load[id]["ventas"][str(nextID)] = detalles
    with open(str(nameDB) + ".json", 'w') as file2:
        json.dump(load, file2, indent=4)

def buscarVenta(nameDB, sucursal, id):
    ''' Permite buscar una venta por su id '''
    sucursal = str(sucursal)
    id = str(id)
    with open(str(nameDB) + ".json", 'r') as file:
            load = json.load(file)
    
    if not(sucursal in load):
        print("No existe esa sucursal!")
        return None
    if not(load[sucursal]["ventas"]):
        print("Esa sucursal no tiene ventas!")
        return None
    if not(id in load[sucursal]["ventas"]):
        print("Esa venta no existe!")
        return None
    
    return load[sucursal]["ventas"][id]
    
    

baseDatos = "BaseDatos"
sucursales = "Sucursales"

# createNewDB("Sucursales") # Ya no es peligrosa

# addProduct("BaseDatos", 1, "Comoda", "Comoda", 1399, None, 10, "Ropa", ["URL1", "URL2"])
# addProduct("BaseDatos", 2, "Mesa", "Mesa", 1799, None, 10, "Hogar", ["URL1", "URL2"])

# print(getProduct("BaseDatos", 2))

# deleteProduct("BaseDatos", "c")

# print(getMultipleProducts(baseDatos, [1, 2, 3]))

# print (getAllProducts(baseDatos))
# editProduct(baseDatos, "1", {"nombre": "emanuel gay"})

# getNextID(baseDatos)
# nuevaVenta(sucursales, 1, {"Producto": "Computadoras", "Cantidad": 1})
# crearSucursal("Sucursales", 1, {"nombre": "Ucasal", "Compañeros":"Gays"})
# editarSucursal(sucursales, 1, {"nombre": "Ucapop", "Productos": ["Libros", "Computadoras"]})
# eliminarSucursal(sucursales, 1)

# print(buscarVenta(sucursales, 1, 1))