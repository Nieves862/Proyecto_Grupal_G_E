import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Establece la conexión a la base de datos y retorna la conexión."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',         
            user='root',       
            password='root', 
            database='gestion_usuarios',
            port=3306  # El puerto debe ser un número entero
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
obtener_conexion()