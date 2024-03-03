from Utils import *
from graphics import balance_graphics,get_graphics


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



def get_balance_resourcer_by_partition(data: list[list[Balance]]):
    """
        This function performs statistical analysis on a list of Experiment objects.
        It groups the data by id and calculates the mean, median, variance, standard deviation,
        minimum and maximum for each group.

        Parameters:
        data (list[Experiment]): A list of Experiment objects.

        Returns:
        list: Six lists containing the mean, median, variance, standard deviation, minimum and maximum
        of the balance for each group, respectively.
        """
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
    # Dar espacio
    return media, mediana, varianza, desviacion_estandar, minimo, maximo




def balance_analize(data: list[Experiment]):
    # extraer cuanto es el número máximo de balances
    count_max_balance = max([len(k.balance) for k in data])
    balance = [k.balance for k in data]
    # agrupar por particiones de tiempo
    media, mediana, varianza, desviacion_estandar, minimo, maximo = get_balance_resourcer_by_partition(balance)

    # analizar con respecto a los valores promedio y mediana
    # espacio
    space()
    print("Analizar en base a la mediana")
    get_analysis(mediana, "Análisis en base a la mediana de los balances en particiones por índices :")
    # por promedio
    balance_graphics(range(0, count_max_balance), mediana, "Balance de la mediana a traves de la cant de los balances")

    # espacio
    space()
    print("Analizar en base al promedio")
    get_analysis(media, "Análisis en base al promedio de los balances en particiones por índices")
    balance_graphics(range(0, count_max_balance), media, "Balance del promedio a traves de la cant de los balances")

    # espacio
    space()
    print("Analizar en base a la varianza")
    get_analysis(varianza, "Análisis en base a la varianza de los balances en particiones por índices")
    balance_graphics(range(0, count_max_balance), varianza,
                     "Balance de la varianza a traves de la cant de los balances")
    # espacio
    space()

    # espacio
    space()
    print("Analizar en base a la desviación estándar")
    get_analysis(desviacion_estandar, "Análisis en base a la desviación estándar de los balances en particiones por índices")
    balance_graphics(range(0, count_max_balance), desviacion_estandar,
                     "Balance de la desviación estándar a traves de la cant de los balances")
    # espacio
    space()
    print("Analizar en base al mínimo")
    get_analysis(minimo, "Análisis en base al mínimo de los balances en particiones por índices")
    balance_graphics(range(0, count_max_balance), minimo, "Balance del mínimo a traves de la cant de los balances")
    # espacio
    space()
    print("Analizar en base al máximo")
    get_analysis(maximo, "Análisis en base al máximo de los balances en particiones por índices")
    balance_graphics(range(0, count_max_balance), maximo, "Balance del máximo a traves de la cant de los balances")
    # espacio
    space()
