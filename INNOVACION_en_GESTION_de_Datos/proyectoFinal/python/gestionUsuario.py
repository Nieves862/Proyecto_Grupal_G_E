import pickle

def cargar_datos(archivo):
    """Carga datos desde un archivo usando pickle."""
    try:
        with open(archivo, 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return []

def guardar_datos(archivo, datos):
    """Guarda datos en un archivo usando pickle."""
    with open(archivo, 'wb') as file:
        pickle.dump(datos, file)
    print("Datos guardados correctamente.")
