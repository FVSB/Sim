import numpy as np
from Utils import *
from balance_analize import *
import matplotlib.pyplot as plt
from graphics import get_graphics


def normal_analize(data: list[Experiment]):
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


from person_analize import *


def analysis(data: list[Experiment]):
    # análisis tipicos y elementales
    normal_analize(data)
    # análisis de balances
    balance_analize(data)
