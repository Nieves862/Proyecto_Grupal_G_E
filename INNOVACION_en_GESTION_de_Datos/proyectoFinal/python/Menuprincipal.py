from gestionAcceso import guardar_accesos
from sistematf import Acceso, Sistema
from datetime import datetime
import registrospluviales

def menu_principal():
    sistema = Sistema()

    while True:
        print("\nMenú Principal")
        print("1. Usuarios y Accesos de la Aplicación")
        print("2. Ordenamiento y Búsqueda de Usuarios")
        print("3. Gestion de base de datos") 
        print("4. Gestionar Registros Pluviales")
        print("5. Salir de la aplicación")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            menu_usuarios_y_accesos(sistema)
        elif opcion == "2":
            menu_ordenamiento_y_busqueda(sistema)
        elif opcion == "3":
            menu_ingreso_sistema(sistema)
        elif opcion == "4":
            submenu_registros_pluviales() 
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intenta nuevamente.")

def menu_usuarios_y_accesos(sistema):
    while True:
        print("\nUsuarios y Accesos")
        print("1. Agregar un nuevo usuario")
        print("2. Modificar un usuario")
        print("3. Eliminar un usuario")
        print("4. Mostrar datos de accesos")
        print("5. Mostrar logs de intentos fallidos")
        print("6. Ingresar al sistema")
        print("7. Volver al Menú principal")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            username = input("Username: ")
            password = input("Password: ")
            email = input("Email: ")
            dni = input("DNI: ")
            sistema.agregar_usuario(username, dni, password, email)
        elif opcion == "2":
            dni = input("Ingresa el DNI del usuario a modificar: ")
            nuevo_username = input("Nuevo username (dejar en blanco si no quieres cambiarlo): ")
            nuevo_password = input("Nuevo password (dejar en blanco si no quieres cambiarlo): ")
            nuevo_email = input("Nuevo email (dejar en blanco si no quieres cambiarlo): ")
            sistema.modificar_usuario(dni, nuevo_username, nuevo_password, nuevo_email)
        elif opcion == "3":
            dni = input("Ingresa el DNI del usuario a eliminar: ")
            sistema.eliminar_usuario(dni)
        elif opcion == "4":
            sistema.mostrar_accesos()
        elif opcion == "5":
            sistema.mostrar_logs()
        elif opcion == "6":
            username = input("Username: ")
            password = input("Password: ")
            if sistema.login(username, password):
                usuario = sistema.buscar_usuario_por_username(username)
                sistema.registrar_acceso(usuario)
                print("Acceso registrado exitosamente.")
                while True:
                    print("\n1. Volver al menú principal")
                    print("2. Salir del sistema")
                    opcion_salida = input("Elige una opción: ")
                    if opcion_salida == "1":
                        break
                    elif opcion_salida == "2":
                        exit()
                    else:
                        print("Opción no válida.")
            else:
                print("Error al iniciar sesión.")
        elif opcion == "7":
            break  
        else:
            print("Opción no válida. Intenta nuevamente.")

def menu_ordenamiento_y_busqueda(sistema):
    while True:
        print("\nOrdenamiento y Búsqueda de Usuarios")
        print("1. Ordenar usuarios por username")
        print("2. Buscar usuario por DNI")
        print("3. Busqueda usuario por username")
        print("4. Busqueda usuario por email")
        print("5. Mostrar todos los usuarios")
        print("6. Volver al Menú principal")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            sistema.usuarios.sort(key=lambda usuario: usuario.get_username())
            sistema.guardar_datos("usuarios.ispc", sistema.usuarios)
            print("Usuarios ordenados por Username:")
            for usuario in sistema.usuarios:
                print(usuario.get_username())
        elif opcion == "2":
            dni = input("Ingrese el DNI a buscar: ")
            usuario = sistema.buscar_usuario(dni)
            if usuario:
                print(usuario)
            else:
                print("Usuario no encontrado.")
        elif opcion == "3":
            username = input("Ingrese el Email a buscar: ")
            usuario = sistema.buscar_usuario_por_username(username)
            if usuario:
                print(usuario)  # Mostrar los datos del usuario encontrado
            else:
                print("Usuario no encontrado.")
        elif opcion == "4":
            email = input("Ingrese el Email a buscar: ")
            usuario = sistema.buscar_usuario_por_email(email)
            if usuario:
                print(usuario)  # Mostrar los datos del usuario encontrado
            else:
                print("Usuario no encontrado.")
        elif opcion == "5":
            sistema.mostrar_todos_usuarios()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intenta nuevamente.")

def menu_ingreso_sistema(sistema):
    username = input("Username: ")
    password = input("Password: ")
    if sistema.login(username, password):
        usuario = sistema.buscar_usuario_por_username(username)
        acceso = Acceso(len(sistema.accesos) + 1, usuario)
        sistema.accesos.append(acceso)
        guardar_accesos("accesos.ispc", sistema.accesos)
        print("Acceso registrado con éxito.")
    else:
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.now()} - Intento fallido: Usuario: {username}, Password: {password}\n")
            print("Registro de intento fallido guardado.")

def submenu_registros_pluviales():
    """Submenú para gestionar registros pluviales."""
    while True:
        print("\nSubmenú - Gestión de Registros Pluviales")
        print("1. Generar registros pluviales aleatorios y guardar en CSV")
        print("2. Cargar registros pluviales desde CSV")
        print("3. Mostrar registros de un mes")
        print("4. Graficar lluvias anuales")
        print("5. Graficar dispersión de lluvias")
        print("6. Graficar porcentaje de lluvias por mes")
        print("7. Volver al menú principal")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            ano = input("Ingrese el año para generar los registros: ")
            registros = registrospluviales.generar_registros_aleatorios()
            registrospluviales.guardar_registros_en_csv(ano, registros)

        elif opcion == "2":
            ano = input("Ingrese el año de los registros que desea cargar: ")
            registrospluviales.cargar_registros_desde_csv(ano)

        elif opcion == "3":
            ano = input("Ingrese el año de los registros: ")
            mes = input("Ingrese el mes (Ej: Enero, Febrero): ").capitalize()
            df = registrospluviales.cargar_registros_desde_csv(ano)
            registrospluviales.mostrar_registros_por_mes(df, mes)

        elif opcion == "4":
            ano = input("Ingrese el año de los registros: ")
            df = registrospluviales.cargar_registros_desde_csv(ano)
            registrospluviales.graficar_lluvias_anuales(df)

        elif opcion == "5":
            ano = input("Ingrese el año de los registros: ")
            df = registrospluviales.cargar_registros_desde_csv(ano)
            registrospluviales.graficar_dispersión(df)

        elif opcion == "6":
            ano = input("Ingrese el año de los registros: ")
            df = registrospluviales.cargar_registros_desde_csv(ano)
            registrospluviales.graficar_lluvias_pie(df)

        elif opcion == "7":
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()
