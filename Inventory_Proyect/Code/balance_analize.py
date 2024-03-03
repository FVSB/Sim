from Utils import *
from graphics import balance_graphics, get_graphics


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
    sales_dict = {}
    for exp in balances:
        for balance in exp:
            if balance.id not in balance_dict:
                balance_dict[balance.id] = []
                sales_dict[balance.id] = []
            balance_dict[balance.id].append(balance)
            sales_dict[balance.id].append(balance.count_sales)
    return balance_dict, sales_dict


def get_balance_resourcer_by_partition(dic: dict):
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

def get_sales_resourcer_by_partition(dic: dict):
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
        media.append(np.mean(dic[key]))

        # Calcula la mediana
        mediana.append(np.median(dic[key]))

        # Calcula la varianza
        varianza.append(np.var(dic[key]))

        # Calcula la desviación estándar
        desviacion_estandar.append(np.std(dic[key]))

        # Calcula el valor mínimo
        minimo.append(np.min(dic[key]))

        # Calcula el valor máximo
        maximo.append(np.max(dic[key]))
    # Dar espacio
    return media, mediana, varianza, desviacion_estandar, minimo, maximo
def __balance_by_Id(balance: list[list[Balance]], count_max_balance: int):
    # agrupar por particiones de tiempo

    # agrupar la data
    dic, sales_dict = group_balances_by_id(balance)
    x = [dic, sales_dict]
    name = [" los balances", " las ventas hasta el balance"]
    for index, (i, j) in enumerate(zip(x, name)):
        if index==0:
            media, mediana, varianza, desviacion_estandar, minimo, maximo = get_balance_resourcer_by_partition(i)
        else:
            media, mediana, varianza, desviacion_estandar, minimo, maximo=get_sales_resourcer_by_partition(i)
        # analizar con respecto a los valores promedio y mediana
        # espacio
        space()
        print("Analizar en base a la mediana")
        get_analysis(mediana, f"Análisis en base a la mediana de {j} en particiones por índices :")
        # por promedio
        balance_graphics(range(0, count_max_balance), mediana,
                         f"Balance de la mediana a traves de la cant de {j}")

        # espacio
        space()
        print("Analizar en base al promedio")
        get_analysis(media, f"Análisis en base al promedio de los {j} en particiones por índices")
        balance_graphics(range(0, count_max_balance), media, f"Balance del promedio a traves de la cant de los {j}")

        # espacio
        space()
        print("Analizar en base a la varianza")
        get_analysis(varianza, f"Análisis en base a la varianza de los {j} en particiones por índices")
        balance_graphics(range(0, count_max_balance), varianza,
                         f"Balance de la varianza a traves de la cant de los {j}")
        # espacio
        space()

        # espacio
        space()
        print("Analizar en base a la desviación estándar")
        get_analysis(desviacion_estandar,
                     f"Análisis en base a la desviación estándar de los {j} en particiones por índices")
        balance_graphics(range(0, count_max_balance), desviacion_estandar,
                         f"La desviación estándar a traves de la cant de {j}")
        # espacio
        space()
        print("Analizar en base al mínimo")
        get_analysis(minimo, f"Análisis en base al mínimo de los {j} en particiones por índices")
        balance_graphics(range(0, count_max_balance), minimo, f"Balance del mínimo a traves de la cant de {j}")
        # espacio
        space()
        print("Analizar en base al máximo")
        get_analysis(maximo, f"Análisis en base al máximo de {j} en particiones por índices")
        balance_graphics(range(0, count_max_balance), maximo, f"Balance del máximo a traves de la cant de {j}")
        # espacio
        space()


def balance_analize(data: list[Experiment]):
    # extraer cuanto es el número máximo de balances
    count_max_balance = max([len(k.balance) for k in data])
    balance = [k.balance for k in data]
    # Balance por el id basado particionar por el Id
    __balance_by_Id(balance, count_max_balance)
