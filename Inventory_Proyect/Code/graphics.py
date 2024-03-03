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



def balance_graphics(time, balance, info: str):
    # Generar gráficos
    plt.figure(figsize=(24, 12))

    # Gráfico de línea del balance a lo largo del tiempo
    plt.subplot(1, 2, 1)
    plt.plot(time, balance)
    plt.xlabel('Tiempo')
    plt.ylabel('Balance')
    plt.title(info)

    # Histograma de los balances
    plt.subplot(1, 2, 2)
    plt.hist(balance, bins=10, edgecolor='black')
    plt.xlabel('Balance')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de los balances')

    plt.tight_layout()
    plt.show()

