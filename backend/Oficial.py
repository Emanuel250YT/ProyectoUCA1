''' Archivo main para gestión de productos '''
import json
import os

def createNewDB(name):
    ''' Crea una nueva base de datos .JSON '''
    with open(str(name)+".json", 'w') as file:
        json.dump({}, file)

def addProduct(nameDB, id, name, desc, price, descuento, stock, categ, images):
    ''' Permite añadir un nuevo producto a la base de datos especificada'''
    data = {"id" : id,  
            "descripcion": desc, 
            "precio": price, 
            "descuento": descuento,
            "stock": stock, 
            "categoria": categ,
            "imagenes": images} # Cargar dict o enlace a una imagen predefinida.
    
    with open(str(nameDB)+".json", 'r+') as file:
        a = json.load(file)
        a[str(name)] = data
        file.seek(0)
        json.dump(a, file, indent=4)

createNewDB("BaseDatos") # Función PELIGROSISIMA (no ejecutar mas de una vez)

# addProduct("BaseDatos", 1, "c", "Comoda", 1399, None, 10, "Ropa", ["URL1", "URL2"])
