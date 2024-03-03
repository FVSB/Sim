import numpy as np

from Utils import *

from graphics import general_graphics, person_graphics, get_graphics


def __particular_analysis(data: list[Person], i: int, do_print: bool):
    title = [f"El análisis de la persona {i} en cuanto quiso comprar",
             f"El análisis de la persona {i} en base a cuantas veces pudo comprar",
             f"El análisis de la persona {i} en base a cuanto se demoró"]
    lis = []
    # intento comprar
    count_to_buy = np.array([a.count_to_buy for a in data])
    x = get_analysis(count_to_buy, title[0], do_print)

    lis.append(x)
    general_graphics(range(0, len(data)), count_to_buy,
                     f"Análisis de la persona {i} en base a cuantas veces pudo comprar y cuanto quiso comprar",
                     xlabel="Cantidad de veces que intentó comprar",
                     ylabel="Cantidad de producto que intentó comprar")

    # pudo comprar

    count_can_buy = np.array([a.count_can_buy for a in data])
    lis.append(get_analysis(count_can_buy, title[1], do_print))
    general_graphics(range(0, len(data)), count_can_buy,
                     f"Análisis de la persona {i} en base a cuantas veces pudo comprar y cuanto pudo comprar",
                     xlabel="Cantidad de veces que intentó comprar",
                     ylabel="Cantidad de producto que pudo comprar")

    # tiempo que se demoró en total
    process_time = np.array([a.departure_time-a.arrival_time for a in data])
    lis.append(get_analysis(process_time, title[2], do_print))
    general_graphics(range(0, len(data)), process_time,
                     f"Análisis de la persona {i} en base a cuanto se demoró",
                     xlabel="Cantidad de veces que intentó comprar",
                     ylabel="Cantidad tiempo que le tomó")

    # Graficar en base a la cantidad de veces que pudo comprar y cuanto quiso comprar
    # hacer el análisis de cada persona
    return title, lis


def person_analize(data: list[Experiment]):
    """"
    HAcer el análisis del las personas en base a cuanto pudo comprar en cada experimento
    cuanto se demoro
    cuando entro
    cuantas veces se fue sin comprar nada
    cual es el promedio que pudo comprar

    """
    # particionar cada uno por ID
    dic_id_person: dict[int:list[Person]] = {}

    for i in data:
        for persons in i.people:
            if persons.id not in dic_id_person:
                dic_id_person[persons.id] = [persons]
            else:
                dic_id_person[persons.id].append(persons)

    average_time = []
    # hacer el análisis
    for index, key in enumerate(dic_id_person.keys()):
        # hacer el análisis de cada persona
        people = dic_id_person[key]
        do_print = False
        if index < 3:
            do_print = True

        title, lis = __particular_analysis(people, index, do_print)  # hacer el análisis de cada persona

        #hacer el  analisis por el conjunto de personas
        # hacer el análisis de cada persona
        media, mediana, varianza, desviacion_estandar, minimo, maximo= lis[2]
        average_time.append(media)

    get_analysis(average_time, "El promedio de tiempo que se demoró cada persona", do_print=True)

