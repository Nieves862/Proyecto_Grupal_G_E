import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sistema_de_transparencia"
            )
            print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def get_connection(self):
        return self.connection

class UserManager:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_user(self):
        try:
            cursor = self.connection.cursor()
            print("\n=== Crear Nuevo Usuario ===")
            
            id_usuario = input("Ingrese ID de Usuario: ")
            nombre = input("Ingrese Nombre del Padre: ")
            password = input("Ingrese Password: ")
            email = input("Ingrese Email: ")
            roles = input("Ingrese Rol (PADRE): ") or "PADRE"
            
            query = """INSERT INTO Usuario 
                    (ID_Usuario, Nombre_Padre, Password, E_mail, creado_En, Estado, Roles) 
                    VALUES (%s, %s, %s, %s, NOW(), 'active', %s)"""
            values = (id_usuario, nombre, password, email, roles)
            
            cursor.execute(query, values)
            self.connection.commit()
            print("Usuario creado exitosamente!")
            
        except Error as e:
            print(f"Error al crear usuario: {e}")
        finally:
            cursor.close()

    def search_user(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            print("\n=== Buscar Usuario ===")
            print("1. Buscar por ID")
            print("2. Buscar por Nombre")
            print("3. Buscar por Email")
            
            option = input("Seleccione una opción: ")
            
            if option == "1":
                search_term = input("Ingrese ID de Usuario: ")
                query = "SELECT * FROM Usuario WHERE ID_Usuario = %s"
            elif option == "2":
                search_term = input("Ingrese Nombre: ")
                query = "SELECT * FROM Usuario WHERE Nombre_Padre LIKE %s"
                search_term = f"%{search_term}%"
            elif option == "3":
                search_term = input("Ingrese Email: ")
                query = "SELECT * FROM Usuario WHERE E_mail = %s"
            else:
                print("Opción inválida")
                return
            
            cursor.execute(query, (search_term,))
            results = cursor.fetchall()
            
            if results:
                for user in results:
                    print("\nUsuario encontrado:")
                    for key, value in user.items():
                        print(f"{key}: {value}")
            else:
                print("No se encontraron usuarios.")
                
        except Error as e:
            print(f"Error al buscar usuario: {e}")
        finally:
            cursor.close()

    def update_user(self):
        try:
            cursor = self.connection.cursor()
            print("\n=== Actualizar Usuario ===")
            
            user_id = input("Ingrese ID del usuario a actualizar: ")
            
            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM Usuario WHERE ID_Usuario = %s", (user_id,))
            if not cursor.fetchone():
                print("Usuario no encontrado.")
                return
            
            print("\nQué desea actualizar?")
            print("1. Nombre")
            print("2. Email")
            print("3. Password")
            print("4. Estado")
            
            option = input("Seleccione una opción: ")
            
            if option == "1":
                new_value = input("Ingrese nuevo nombre: ")
                query = "UPDATE Usuario SET Nombre_Padre = %s WHERE ID_Usuario = %s"
            elif option == "2":
                new_value = input("Ingrese nuevo email: ")
                query = "UPDATE Usuario SET E_mail = %s WHERE ID_Usuario = %s"
            elif option == "3":
                new_value = input("Ingrese nueva password: ")
                query = "UPDATE Usuario SET Password = %s WHERE ID_Usuario = %s"
            elif option == "4":
                new_value = input("Ingrese nuevo estado (active/inactive/deleted): ")
                query = "UPDATE Usuario SET Estado = %s WHERE ID_Usuario = %s"
            else:
                print("Opción inválida")
                return
            
            cursor.execute(query, (new_value, user_id))
            self.connection.commit()
            print("Usuario actualizado exitosamente!")
            
        except Error as e:
            print(f"Error al actualizar usuario: {e}")
        finally:
            cursor.close()

    def delete_user(self):
        try:
            cursor = self.connection.cursor()
            print("\n=== Eliminar Usuario ===")
            
            user_id = input("Ingrese ID del usuario a eliminar: ")
            
            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM Usuario WHERE ID_Usuario = %s", (user_id,))
            if not cursor.fetchone():
                print("Usuario no encontrado.")
                return
            
            confirm = input("¿Está seguro que desea eliminar este usuario? (s/n): ")
            if confirm.lower() == 's':
                cursor.execute("DELETE FROM Usuario WHERE ID_Usuario = %s", (user_id,))
                self.connection.commit()
                print("Usuario eliminado exitosamente!")
            else:
                print("Operación cancelada.")
            
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
        finally:
            cursor.close()

    def login(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            print("\n=== Iniciar Sesión ===")
            
            email = input("Ingrese Email: ")
            password = input("Ingrese Password: ")
            
            query = "SELECT * FROM Usuario WHERE E_mail = %s AND Password = %s AND Estado = 'active'"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
            if user:
                print("\n¡Inicio de sesión exitoso!")
                print("Abriendo gestión de estudiantes...")
                # Aquí iría la llamada al programa de gestión de estudiantes
                return True
            else:
                print("Credenciales inválidas o usuario inactivo.")
                return False
                
        except Error as e:
            print(f"Error en el inicio de sesión: {e}")
            return False
        finally:
            cursor.close()

def main():
    db = DatabaseConnection()
    if db.get_connection() is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    user_manager = UserManager(db.get_connection())
    
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE USUARIOS ===")
        print("1. Gestión Usuarios")
        print("2. Iniciar Sesión")
        print("3. Salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            while True:
                print("\n=== Gestión Usuarios ===")
                print("1. Crear Usuario")
                print("2. Buscar Usuario")
                print("3. Actualizar Usuario")
                print("4. Eliminar Usuario")
                print("5. Volver al Menú Principal")
                
                sub_option = input("\nSeleccione una opción: ")
                
                if sub_option == "1":
                    user_manager.create_user()
                elif sub_option == "2":
                    user_manager.search_user()
                elif sub_option == "3":
                    user_manager.update_user()
                elif sub_option == "4":
                    user_manager.delete_user()
                elif sub_option == "5":
                    break
                else:
                    print("Opción inválida")
        
        elif option == "2":
            if user_manager.login():
                print("Implementar llamada a gestión_Estudiantes aquí")
        
        elif option == "3":
            print("¡Gracias por usar el sistema!")
            db.get_connection().close()
            sys.exit()
        
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
