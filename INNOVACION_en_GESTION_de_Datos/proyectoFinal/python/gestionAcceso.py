import pickle


def cargar_accesos(archivo):
    """Carga los accesos desde un archivo."""
    try:
        with open(archivo, 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return []

def guardar_accesos(archivo, datos):
    """Guarda los accesos en un archivo."""
    with open(archivo, 'wb') as file:
        pickle.dump(datos, file)
