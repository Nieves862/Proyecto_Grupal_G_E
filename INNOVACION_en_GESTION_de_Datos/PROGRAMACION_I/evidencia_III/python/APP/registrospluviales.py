import csv
import os
import random
import pandas as pd
import matplotlib.pyplot as plt

def generar_registros_aleatorios():
    """Genera una lista de listas donde cada sublista representa los días de un mes y contiene datos aleatorios de pluviosidad."""
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # Días en cada mes (sin controlar bisiestos)
    registros = []
    
    for dias in dias_por_mes:
        registros.append([random.uniform(0, 100) for _ in range(dias)])  # Genera valores aleatorios entre 0 y 100 mm
    
    return registros

def guardar_registros_en_csv(ano, registros):
    """Guarda los registros pluviales en un archivo CSV."""
    nombre_archivo = f"registroPluvial{ano}.csv"
    columnas = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    # Crear un DataFrame a partir de los registros pluviales
    df = pd.DataFrame({columna: pd.Series(datos) for columna, datos in zip(columnas, registros)})

    # Guardar en un archivo CSV
    df.to_csv(nombre_archivo, index=False)
    print(f"Datos guardados en {nombre_archivo}")

def cargar_registros_desde_csv(ano):
    """Carga los registros pluviales desde un archivo CSV."""
    nombre_archivo = f"registroPluvial{ano}.csv"
    
    if os.path.exists(nombre_archivo):
        df = pd.read_csv(nombre_archivo)
        print(f"Datos cargados desde {nombre_archivo}")
        return df
    else:
        print(f"Archivo {nombre_archivo} no encontrado, generando datos aleatorios...")
        registros = generar_registros_aleatorios()
        guardar_registros_en_csv(ano, registros)
        # Crear un DataFrame con los datos generados
        columnas = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        df = pd.DataFrame({columna: pd.Series(datos) for columna, datos in zip(columnas, registros)})
        return df

def mostrar_registros_por_mes(df, mes):
    """Muestra los registros de un mes específico."""
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    if mes in meses:
        print(f"Registros de {mes}:")
        print(df[mes].dropna())  # Mostrar los valores no nulos del mes
    else:
        print("Mes inválido. Elija uno de los siguientes:", meses)

def graficar_lluvias_anuales(df):
    """Genera un gráfico de barras de lluvias anuales por mes."""
    # Sumar los valores de cada mes para obtener las lluvias totales del año
    totales = df.sum()

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    totales.plot(kind='bar', color='skyblue')
    plt.title("Lluvias Totales por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Milímetros de Lluvia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_dispersión(df):
    """Genera un gráfico de dispersión donde el eje x son los meses y el eje y los días del mes."""
    plt.figure(figsize=(12, 6))

    # Para cada mes, graficar los días y las lluvias
    for i, mes in enumerate(df.columns):
        dias = df[mes].dropna().index + 1  # Índices de los días (1 a 31)
        lluvias = df[mes].dropna().values  # Valores de lluvia
        plt.scatter([i + 1] * len(lluvias), dias, s=lluvias, alpha=0.5, label=mes)  # Tamaño proporcional a la lluvia

    plt.title("Lluvias Diarias por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Día del Mes")
    plt.xticks(ticks=range(1, 13), labels=df.columns, rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_lluvias_pie(df):
    """Genera un gráfico circular (pie chart) que muestra el porcentaje de lluvia acumulada por mes."""
    totales = df.sum()

    # Crear el gráfico circular
    plt.figure(figsize=(8, 8))
    plt.pie(totales, labels=totales.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Porcentaje de Lluvias por Mes")
    plt.show()

def main():
    ano = input("Ingrese el año del registro pluvial que desea cargar: ")
    
    # Cargar los registros pluviales del año
    df_registros = cargar_registros_desde_csv(ano)
    
    # Pedir el mes para mostrar los registros
    mes = input("Ingrese el nombre del mes (Ejemplo: Enero, Febrero): ").capitalize()
    
    # Mostrar los registros del mes seleccionado
    mostrar_registros_por_mes(df_registros, mes)
    
    # Generar gráficos
    print("Generando gráficos...")
    graficar_lluvias_anuales(df_registros)
    graficar_dispersión(df_registros)
    graficar_lluvias_pie(df_registros)

if __name__ == "__main__":
    main()
