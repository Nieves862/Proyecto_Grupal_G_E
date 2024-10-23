import pickle
from datetime import datetime


class Usuario:
    def __init__(self, id, nombre_usuario, password, e_mail):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.password = password
        self.e_mail = e_mail

    def __str__(self):
        return f"ID: {self.id}, Username: {self.nombre_usuario}, Email: {self.e_mail}"

class Acceso:
    def __init__(self, id, usuario_logueado):
        self.id = id
        self.fecha_ingreso = datetime.now()
        self.fecha_salida = None
        self.usuario_logueado = usuario_logueado

    def registrar_salida(self):
        self.fecha_salida = datetime.now()

    def __str__(self):
        return (f"ID Acceso: {self.id}, Usuario: {self.usuario_logueado.nombre_usuario}, "
                f"Fecha Ingreso: {self.fecha_ingreso}, Fecha Salida: {self.fecha_salida}")

class Sistema:
    def __init__(self):
        self.usuarios = self.cargar_datos("usuarios.ispc")
        self.ultimo_id = len(self.usuarios)
        self.accesos = self.cargar_datos("accesos.ispc")
        self.usuarios_ordenados = False  # Variable para ver si los usuarios están ordenados

    def cargar_datos(self, archivo):
        try:
            with open(archivo, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []

    def guardar_datos(self, archivo, datos):
        with open(archivo, 'wb') as file:
            pickle.dump(datos, file)

    def agregar_usuario(self, nombre_usuario, password, e_mail):
        self.ultimo_id += 1
        nuevo_usuario = Usuario(self.ultimo_id, nombre_usuario, password, e_mail)
        self.usuarios.append(nuevo_usuario)
        self.guardar_datos("usuarios.ispc", self.usuarios)
        print(f"Usuario {nombre_usuario} agregado correctamente.")
        self.usuarios_ordenados = False  # Los usuarios no están ordenados después de agregar uno nuevo

    def modificar_usuario(self, username_o_email, nuevo_username=None, nuevo_password=None, nuevo_email=None):
        usuario = self.buscar_usuario(username_o_email)
        if usuario:
            if nuevo_username:
                usuario.nombre_usuario = nuevo_username
            if nuevo_password:
                usuario.password = nuevo_password
            if nuevo_email:
                usuario.email = nuevo_email
            self.guardar_datos("usuarios.ispc", self.usuarios)
            print(f"Usuario {username_o_email} modificado correctamente.")
        else:
            print(f"Usuario {username_o_email} no encontrado.")
        self.usuarios_ordenados = False  # Si se modifica un usuario pierde el orden

    def eliminar_usuario(self, username_o_email):
        usuario = self.buscar_usuario(username_o_email)
        if usuario:
            self.usuarios.remove(usuario)
            self.guardar_datos("usuarios.ispc", self.usuarios)
            print(f"Usuario {username_o_email} eliminado correctamente.")
        else:
            print(f"Usuario {username_o_email} no encontrado.")
        self.usuarios_ordenados = False  # Si se elimina un usuario se pierde el orden

    def mostrar_todos_usuarios(self):
        if self.usuarios:
            for usuario in self.usuarios:
                print(usuario)
        else:
            print("No hay usuarios registrados.")

    # Opción: Ordenar usuarios por Python usando el método sort() con key por username
    def ordenar_por_sort(self):
        self.usuarios.sort(key=lambda usuario: usuario.nombre_usuario)
        self.guardar_datos("usuarios.ispc", self.usuarios)
        self.usuarios_ordenados = True  # Indicar que los usuarios están ordenados
        print("Usuarios ordenados por Python sort().")

    # Búsqueda secuencial (si los usuarios no están ordenados)
    def buscar_usuario_secuencial(self, nombre_usuario):
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                print("Búsqueda realizada por técnica secuencial.")
                return usuario
        return None

    # Búsqueda binaria (si los usuarios están ordenados)
    def buscar_usuario_binaria(self, nombre_usuario):
        print("Búsqueda realizada por técnica binaria.")
        izquierda, derecha = 0, len(self.usuarios) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if self.usuarios[medio].nombre_usuario == nombre_usuario:
                return self.usuarios[medio]
            elif self.usuarios[medio].nombre_usuario < nombre_usuario:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    # Buscar usuario por username, utilizando la técnica de búsqueda apropiada
    def buscar_usuario(self, username_o_email):
        if self.usuarios_ordenados:
            return self.buscar_usuario_binaria(username_o_email)
        else:
            return self.buscar_usuario_secuencial(username_o_email)

    def registrar_acceso(self, usuario):
        nuevo_acceso = Acceso(len(self.accesos) + 1, usuario)
        self.accesos.append(nuevo_acceso)
        self.guardar_datos("accesos.ispc", self.accesos)
        print(f"Acceso registrado para el usuario {usuario.username}. Fecha de ingreso: {nuevo_acceso.fecha_ingreso}")

    def registrar_intento_fallido(self, username, password):
        with open("logs.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Intento fallido: Usuario: {username}, Password: {password}\n")
        print("Datos incorrectos. Registro de intento fallido guardado.")

    def login(self, nombre_usuario, password):
        """Método para verificar si el usuario puede iniciar sesión"""
        for usuario in self.usuarios:
            if usuario.username == nombre_usuario and usuario.password == password:
                print(f"Bienvenido, {nombre_usuario}. Has ingresado al sistema.")
                # Registrar acceso exitoso
                return True
        # Si no encuentra un usuario válido, registrar el intento fallido
        print("Error: Username o password incorrecto.")
        self.registrar_intento_fallido(nombre_usuario, password)
        return False

