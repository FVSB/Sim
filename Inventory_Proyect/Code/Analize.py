import numpy as np
from Utils import *
import matplotlib.pyplot as plt


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


def get_analysis(data, info: str):
    # Calcula la media
    media = np.mean(data)

    # Calcula la mediana
    mediana = np.median(data)

    # Calcula la varianza
    varianza = np.var(data)

    # Calcula la desviación estándar
    desviacion_estandar = np.std(data)

    # Calcula el valor mínimo
    minimo = np.min(data)

    # Calcula el valor máximo
    maximo = np.max(data)
    print()
    #Dar espacio
    space()
    print(info)
    print(f' Media: {media}')
    print(f'Mediana: {mediana}')
    print(f'Varianza: {varianza}')
    print(f'Desviación estándar: {desviacion_estandar}')
    print(f'Mínimo: {minimo}')
    print(f'Máximo: {maximo}')
    #dar espacio
    space()
    # llamar a graficador
    get_graphics(media, mediana, varianza, desviacion_estandar, minimo, maximo, info, data)


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


def balance_analize_by_experiment(data: list[Balance]):
    # En base al balance
    balance = np.array([k.balance for k in data])
    get_analysis(balance, "El balance fue de:")
    time = np.array([k.time for k in data])
    # graficos en base al tiempo
    balance_graphics(time, balance, "Balance a lo largo del tiempo")

    # En base al flujo de caja
    a = np.array([k.cash_flow for k in data])
    get_analysis(a, "El flujo de caja fue de:")
    balance_graphics(time, a, "Flujo de caja a lo largo del tiempo")

    # en base al tiempo con balance positivo

    time = np.array([k.time for k in data if k.balance > 0])
    get_analysis(time, "El tiempo con balance positivo fue de:")
    # en base al balance positivo
    balance = np.array([k.balance for k in data if k.balance > 0])
    get_analysis(balance, "El balance positivo fue de:")
    # graficar relacion balance positivo con tiempo
    balance_graphics(time, balance, "Balance positivo a lo largo del tiempo")

    # en base al tiempo con balance negativo
    time = np.array([k.time for k in data if k.balance < 0])
    get_analysis(time, "El tiempo con balance negativo fue de:")
    # en base al balance negativo
    balance = np.array([k.balance for k in data if k.balance < 0])
    get_analysis(balance, "El balance negativo fue de:")


def group_balances_by_id(balances: list[list[Balance]]):
    balance_dict = {}

    for exp in balances:
        for balance in exp:
            if balance.id not in balance_dict:
                balance_dict[balance.id] = []
            balance_dict[balance.id].append(balance)
    return balance_dict


def balance_analize(data, count_max_balance: int):
    # agrupar la data
    dic = group_balances_by_id(data)
    # iterar por las particiones de tiempo
    media = []
    mediana = []
    varianza = []
    desviacion_estandar = []
    minimo = []
    maximo = []
    for key in dic.keys():
        # balance_analize_by_experiment(dic[key])
        # Calcula la media
        media.append(np.mean([k.balance for k in dic[key]]))

        # Calcula la mediana
        mediana.append(np.median([k.balance for k in dic[key]]))

        # Calcula la varianza
        varianza.append(np.var([k.balance for k in dic[key]]))

        # Calcula la desviación estándar
        desviacion_estandar.append(np.std([k.balance for k in dic[key]]))

        # Calcula el valor mínimo
        minimo.append(np.min([k.balance for k in dic[key]]))

        # Calcula el valor máximo
        maximo.append(np.max([k.balance for k in dic[key]]))

    # analizar con respecto a los valores promedio y mediana
    #espacio
    space()
    print("Analizar en base a la mediana")
    get_analysis(mediana, "Análisis en base a la mediana de los balances en particiones por índices :")
    # por promedio
    balance_graphics(range(0, count_max_balance), mediana, "Balance de la mediana a traves de la cant de los balances")

    #espacio
    space()
    print("Analizar en base al promedio")
    get_analysis(media, "Análisis en base al promedio de los balances en particiones por índices")
    balance_graphics(range(0, count_max_balance), media, "Balance del promedio a traves de la cant de los balances")

    #espacio
    space()
def analysis(data: list[Experiment]):
    # extraer cuanto es el número máximo de balances
    max_balance = max([len(k.balance) for k in data])
    balance = [k.balance for k in data]
    # analizar los balances en base a los índices
    balance_analize(balance, max_balance)

    # En base a las ganancias de dinero
    a = np.array([k.money_balance for k in data])
    get_analysis(a, "El el balance monetario fue de:")

    # No pudieron comprar
    a = np.array([a.count_persons_cannot_buy for a in data])
    get_analysis(a, "No pudieron comprar nada:")
    # Se suplio la demanda
    a = np.array([a.count_persons_can_buy_all for a in data])
    get_analysis(a, "Se suplió la demanda a:")
    # No fue suplida toda la demanda
    a = np.array([a.count_persons_cannot_buy_all for a in data])
    get_analysis(a, "Fueron suplidos con menos oferta que su demanda")
