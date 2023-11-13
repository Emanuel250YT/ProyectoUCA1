''' Archivo main para gestión de productos '''
import json
import os


def createNewDB(name):
    ''' Crea una nueva base de datos .JSON '''
    with open(str(name)+".json", 'w') as file:
        json.dump({}, file)


def addProduct(nameDB, id, name, desc, price, descuento, stock, categ, noStock):
    ''' Permite añadir un nuevo producto a la base de datos especificada'''
    data = {"id": id,
            "descripcion": desc,
            "precio": price,
            "descuento": descuento,
            "stock": stock,
            "categoria": categ,
            # Cargar dict o enlace a una imagen predefinida.
            "agotado": noStock}

    with open(str(nameDB)+".json", 'r+') as file:
        a = json.load(file)
        a[str(name)] = data
        file.seek(0)
        json.dump(a, file, indent=4)


def getProduct(db, product):
    ''' Permite obtener el diccionario del producto desde la BD'''
    with open(str(db)+".json", 'r') as file:
        load = json.load(file)
        if product in load:
            prodData = load[product]
            return prodData
    return None


def deleteProduct(db, product):
    ''' Permite eliminar un producto mediante su nombre '''
    with open(str(db)+".json", "r+") as file:
        load = json.load(file)
    try:
        load.pop("c")

        with open(str(db)+".json", 'w') as file2:
            json.dump(load, file2, indent=4)
    except KeyError:
        print("No existe tal elemento!")

# createNewDB("BaseDatos") # Función PELIGROSISIMA (no ejecutar mas de una vez)

# addProduct("BaseDatos", 1, "a", "Comoda", 1399, None, 10, "Ropa", ["URL1", "URL2"])

# print(getProduct("BaseDatos", "a"))

# deleteProduct("BaseDatos", "c")
