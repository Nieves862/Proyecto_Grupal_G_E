import pickle
import os
from datetime import datetime
from gestionUsuario import cargar_datos, guardar_datos
from gestionAcceso import cargar_accesos, guardar_accesos

class Usuario:
    def __init__(self, id, username, dni, password, email):
        self.__id = id
        self.__username = username
        self.__dni = dni
        self.__password = password
        self.__email = email

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_dni(self):
        return self.__dni

    def set_dni(self, dni):
        self.__dni = dni

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def __str__(self):
        return f"ID: {self.__id}, Username: {self.__username}, Email: {self.__email}, DNI: {self.__dni}"

class Acceso:
    def __init__(self, id, usuario_logueado):
        self.__id = id
        self.__fecha_ingreso = datetime.now()
        self.__fecha_salida = None
        self.__usuario_logueado = usuario_logueado

    def registrar_salida(self):
        self.__fecha_salida = datetime.now()

    def __str__(self):
        return (f"ID Acceso: {self.__id}, Usuario: {self.__usuario_logueado.get_username()}, "
                f"Fecha Ingreso: {self.__fecha_ingreso}, Fecha Salida: {self.__fecha_salida}")

class Sistema:
    def __init__(self):
        self.usuarios = cargar_datos("usuarios.ispc")
        self.accesos = cargar_accesos("accesos.ispc")
        self.usuarios_ordenados = False

    def agregar_usuario(self, username, dni, password, email):
        nuevo_usuario = Usuario(len(self.usuarios) + 1, username, dni, password, email)
        self.usuarios.append(nuevo_usuario)
        self.usuarios.sort(key=lambda usuario: usuario.get_dni())
        guardar_datos("usuarios.ispc", self.usuarios)  # Asegúrate de pasar el segundo argumento
        print(f"Usuario {username} agregado correctamente.")

    def modificar_usuario(self, dni, nuevo_username=None, nuevo_password=None, nuevo_email=None):
        usuario = self.buscar_usuario(dni)
        if usuario:
            if nuevo_username:
                usuario.set_username(nuevo_username)
            if nuevo_password:
                usuario.set_password(nuevo_password)
            if nuevo_email:
                usuario.set_email(nuevo_email)
            self.guardar_datos("usuarios.ispc", self.usuarios)  # Corrige aquí pasando self.usuarios
            print(f"Usuario {dni} modificado correctamente.")
        else:
            print(f"Usuario {dni} no encontrado.")


    def eliminar_usuario(self, dni):
        usuario = self.buscar_usuario(dni)
        if usuario:
            self.usuarios.remove(usuario)
            self.guardar_datos("usuarios.ispc", self.usuarios)  # Corrige aquí pasando self.usuarios
            print(f"Usuario {dni} eliminado correctamente.")
        else:
            print(f"Usuario {dni} no encontrado.")



    def buscar_usuario_por_username(self, username):
        for usuario in self.usuarios:
            if usuario.get_username() == username:
                return usuario
        return None
    
    def buscar_usuario(self, dni):
        """Busca un usuario por su DNI."""
        for usuario in self.usuarios:
            if usuario.get_dni() == dni:
                return usuario
        return None
    
    def buscar_usuario_por_email(self, email):
        """Busca un usuario por su email."""
        for usuario in self.usuarios:
            if usuario.get_email() == email:
                return usuario
        return None
    
    def registrar_acceso(self, usuario):
        nuevo_acceso = Acceso(len(self.accesos) + 1, usuario)
        self.accesos.append(nuevo_acceso)
        guardar_accesos("accesos.ispc", self.accesos)
        print(f"Acceso registrado para el usuario {usuario.get_username()}.")

    def mostrar_accesos(self):
        if self.accesos:
            for acceso in self.accesos:
                print(acceso)
        else:
            print("No hay registros de accesos.")
            
    def guardar_datos(self, archivo, datos):
        with open(archivo, "wb") as f:
            pickle.dump(datos, f)  
        print("Datos guardados correctamente.")
            
    def mostrar_logs(self):
        """Muestra los logs de intentos fallidos."""
        try:
            with open("logs.txt", "r") as log_file:
                print(log_file.read())
        except FileNotFoundError:
            print("No hay logs de intentos fallidos.")
    
    def mostrar_todos_usuarios(self):
        """Muestra todos los usuarios registrados."""
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return

        print("\nLista de Usuarios:")
        for usuario in self.usuarios:
            print(usuario)
    def registrar_intento_fallido(self, username, password):
        """Registra un intento fallido de inicio de sesión en el archivo de logs."""
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.now()} - Intento fallido: Usuario: {username}, Password: {password}\n")
            
    def login(self, username, password):
        for usuario in self.usuarios:
            if usuario.get_username() == username and usuario.get_password() == password:
                print(f"Bienvenido, {username}. Has ingresado al sistema.")
                return True  # Cambiado para retornar True al encontrar usuario
        print("Error: Username o password incorrecto.")
        self.registrar_intento_fallido(username, password)
        return False  


            
def ordenar_usuarios(usuarios):
    """Ordena la lista de usuarios por username y guarda el resultado en un archivo."""
    if not usuarios:
        print("No hay usuarios para ordenar.")
        return None  # Retorna None si no hay usuarios

    usuarios.sort(key=lambda usuario: usuario.username)
    guardar_usuarios_ordenados(usuarios)
    return usuarios  # Retorna la lista ordenada

def guardar_usuarios_ordenados(usuarios):
    """Guarda la lista de usuarios ordenados en un archivo."""
    try:
        with open("usuariosOrdenadosPorUsername.ispc", "wb") as file:
            pickle.dump(usuarios, file)
        print("Usuarios ordenados y guardados con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al guardar usuarios: {e}")