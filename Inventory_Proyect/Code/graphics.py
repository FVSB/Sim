import matplotlib.pyplot as plt
import numpy as np


def get_graphics(media, mediana, varianza, desviacion_estandar, minimo, maximo, info, data):
    # Crea una lista con los nombres de las estadísticas
    stats = ['Media', 'Mediana', 'Varianza', 'Desviación estándar', 'Mínimo', 'Máximo']

    # Crea una lista con los valores de las estadísticas
    values = [media, mediana, varianza, desviacion_estandar, minimo, maximo]

    # Crea un gráfico de barras
    plt.bar(stats, values)

    # Añade un título y etiquetas a los ejes
    plt.title(info)
    plt.xlabel('Estadísticas')
    plt.ylabel('Valores')

    # Muestra el gráfico
    plt.show()

    # Crea un histograma
    plt.hist(data, bins=10, edgecolor='black')

    # Añade un título y etiquetas a los ejes
    plt.title('Distribución de los datos')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')

    # Muestra el gráfico
    plt.show()


def general_graphics(time, balance, info: str, xlabel: str, ylabel: str):
    """"
    el xlabel es para relacionar el tiempo
    el ylabel es para relacionar el otro ente
    """
    # Generar gráficos
    plt.figure(figsize=(24, 12))

    # Gráfico de línea del balance a lo largo del tiempo
    plt.subplot(1, 2, 1)
    plt.plot(time, balance)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(info)

    # Histograma de los balances
    plt.subplot(1, 2, 2)
    plt.hist(balance, bins=10, edgecolor='black')
    plt.xlabel(ylabel)
    plt.ylabel('Frecuencia')
    plt.title(f'Distribución de los {ylabel}')

    plt.tight_layout()
    plt.show()


def balance_graphics(time, balance, info: str):
    general_graphics(time, balance, info, "Tiempo", "Balance")

def person_graphics(time,balance,info:str):

    general_graphics(time, balance, info, "Tiempo", "Persona")