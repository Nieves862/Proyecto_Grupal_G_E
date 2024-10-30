from Sistemaev3 import Sistema
import registrospluviales  

def menu_principal():
    sistema = Sistema()

    while True:
        print("\nMenú Principal")
        print("1. Agregar un nuevo usuario")
        print("2. Modificar un usuario")
        print("3. Eliminar un usuario")
        print("4. Buscar un usuario por username o email")
        print("5. Mostrar todos los usuarios")
        print("6. Ordenar usuarios por username")  
        print("7. Ingresar al sistema")
        print("8. Gestionar Registros Pluviales")  
        print("9. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            usuario_nombre = input("Username: ")
            password = input("Password: ")
            e_mail = input("Email: ")
            sistema.agregar_usuario(usuario_nombre, password, e_mail)

        elif opcion == "2":
            username_o_email = input("Ingresa el username o email del usuario a modificar: ")
            nuevo_username = input("Nuevo username (dejar en blanco si no quieres cambiarlo): ")
            nuevo_password = input("Nuevo password (dejar en blanco si no quieres cambiarlo): ")
            nuevo_email = input("Nuevo email (dejar en blanco si no quieres cambiarlo): ")
            sistema.modificar_usuario(username_o_email, nuevo_username, nuevo_password, nuevo_email)

        elif opcion == "3":
            username_o_email = input("Ingresa el username o email del usuario a eliminar: ")
            sistema.eliminar_usuario(username_o_email)

        elif opcion == "4":
            username_o_email = input("Ingresa el username o email del usuario a buscar: ")
            usuario = sistema.buscar_usuario(username_o_email)
            if usuario:
                print(usuario)
            else:
                print(f"Usuario {username_o_email} no encontrado.")

        elif opcion == "5":
            sistema.mostrar_todos_usuarios()

        elif opcion == "6": 
            sistema.ordenar_por_sort()

        elif opcion == "7":  
            usuario_nombre = input("Username: ")
            password = input("Password: ")
            if sistema.login(usuario_nombre, password):  
                usuario = sistema.buscar_usuario(usuario_nombre)  
                sistema.registrar_acceso(usuario)  
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

        elif opcion == "8":  
            submenu_registros_pluviales()  
        elif opcion == "9":  
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")


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
