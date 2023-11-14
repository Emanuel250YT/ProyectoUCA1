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
    

baseDatos = "BaseDatos"

# createNewDB("Sucursales") # Ya no es peligrosa

# addProduct("BaseDatos", 1, "Comoda", "Comoda", 1399, None, 10, "Ropa", ["URL1", "URL2"])
# addProduct("BaseDatos", 2, "Mesa", "Mesa", 1799, None, 10, "Hogar", ["URL1", "URL2"])

# print(getProduct("BaseDatos", 2))

# deleteProduct("BaseDatos", "c")


# print (getAllProducts(baseDatos))
# editProduct(baseDatos, "1", {"nombre": "emanuel gay"})
