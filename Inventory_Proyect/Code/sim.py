import random
import math
import simpy

# Constants
SEMILLA = 30
# cant de tenderos
NUM_TENDEROS = 1
# tiempo de llegada promedio entre cada cliente osea un promedio de 3 por hora
T_LLEGADAS = 20
# minutos  12 horas
TIEMPO_SIMULACION = 720.0
# cant de productos inicialmente en stock
STOCK_INICIAL = 100
# cant maxima de productos en stock
STOCK_MAX = 10
# cant minima de productos en stock
STOCK_MIN = 2
# precio de producto a comprar al proveedor
PRECIO_COMPRA = 2
# precio de producto a vender al cliente
PRECIO_VENTA = 3
# precio mantener una unidad de producto en stock en una unidad de tiempo
PRECIO_MANTENIMIENTO = 0.5
# Cant maxima de clientes a ver en la simulacion
TOT_CLIENTES = 3000
# Tiempo Máximo en reponer
Repo_Max_T = 180
# Tiempo Minimo en reponer
Repo_Min_T = 65
# variables

# cant de productos en stock en momento i
stock = 1
# cant de productos vendidos
vendidos = 0
# cant de productos comprados al proveedor
comprados = 0
# balance dinero en caja
balance = 0
# ultimo tiempo de compra
last_time_compra = 0
# Se vendio el ultimo
last_sale_ok = False
te = 0.0  # tiempo de espera total
dt = 0.0  # duracion de servicio total
fin = 0.0  # minuto en el que finaliza


# funciones
def hay_que_comprar() -> bool:
    global stock
    if stock < STOCK_MIN:
        return True
    else:
        return False


def comprar(env, cantidad):
    
    global stock
    global balance
    global comprados
    global last_time_compra
    stock += cantidad
    balance -= cantidad * PRECIO_COMPRA
    comprados += cantidad
    print("Compra %.2f unidades en minuto %.2f" % (cantidad, env.now))

    R = random.random()  # Obtiene un numero aleatorio y lo guarda en R
    tiempo = Repo_Max_T - Repo_Min_T
    tiempo_compra = Repo_Min_T + (tiempo * R)  # Distribucion uniforme
    yield env.timeout(tiempo_compra)  # deja correr el tiempo n minutos
    last_time_compra = env.now
    print("  Compra listo en %.2f minutos tiempo actual %.2f" % (tiempo_compra, env.now))


def tiempo_atención(negar=False):  # Distribución de probabilidad de tiempo de atención
    tiempo_maximo = 5.0
    tiempo_minimo = 0.7
    if negar == True:
        tiempo_maximo = 1.0
        tiempo_minimo = 0.3

    R = random.random()
    return tiempo_minimo + (tiempo_maximo - tiempo_minimo) * R  # Distribución uniforme


def vender(name, env, last_sale_ok=[False]):
    global stock
    global balance
    global vendidos
    global dt

    cantidad = random.randint(1, 10)
    if cantidad < 1 or cantidad > stock:
        # No se puede vender
        # llamar al evento mandar a pedir
        time = tiempo_atención(negar=True)
        dt = dt + time
        
        last_sale_ok[0] = False
        yield env.timeout(time)  # Deja correr el tiempo n minutos
    else:
        stock -= cantidad
        balance += cantidad * PRECIO_VENTA
        vendidos += cantidad
        print("Venta %.2f unidades en minuto %.2f al cliente %s " % (cantidad, env.now, name))
        time = tiempo_atención(negar=True)

        dt = dt + time
        # Fue exitosa la venta
        last_sale_ok[0] = True
        yield env.timeout(time)  # Deja correr el tiempo n minutos


def cliente(env, name, personal):
    global te
    global fin
    llega = env.now  # Guarda el minuto de llegada del cliente
    print("---> %s llego a la tienda en minuto %.2f" % (name, llega))

    with personal.request() as request:  # Espera su turno
        yield request  # Obtiene turno
        pasa = env.now  # Guarda el minuto cuado comienza a ser atendido
        espera = pasa - llega  # Calcula el tiempo que espero
        te = te + espera  # Acumula los tiempos de espera
        print("**** %s pasa con el tendero en minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
        # Vender producto
        # Si el producto Se pudo comprar se continua
        sale_bool = [False]
        yield env.process(vender(name, env, sale_bool))  # Invoca al proceso vender
        ok_sale = sale_bool[0]
        #assert ok_sale, f"El cliente {name} no pudo comprar el producto "
        print(f"LA venta al cliente {name} fue exitosa {ok_sale}    ")
        # El cliente termina la compra
        deja = env.now
        print("<--- %s deja la tienda en minuto %.2f" % (name, deja))

        yield env.timeout(ok_sale)
    if not ok_sale:
        # No se pudo vender
        print("**** %s no se pudo vender" % (name))
        yield env.process(comprar(env, STOCK_MAX - stock))  # Invoca al proceso comprar al distribuidor
    if hay_que_comprar():
        # Comprar al distribuidor
        yield env.process(comprar(env, STOCK_MAX - stock))

        fin = env.now  # Conserva globalmente el ultimo minuto de la simulacion


def principal(env, personal):
    llegada = 0
    i = 0
    for i in range(TOT_CLIENTES):  # Para n clientes
        R = random.random()
        llegada = -T_LLEGADAS * math.log(R)  # Distribucion exponencial
        yield env.timeout(llegada)  # Deja transcurrir un tiempo entre uno y otro
        i += 1
        env.process(cliente(env, 'Cliente %d' % i, personal))


print("------------------- Bienvenido Simulacion Inventario ------------------")
random.seed(SEMILLA)  # Cualquier valor
env = simpy.Environment()  # Crea el objeto entorno de simulacion
personal = simpy.Resource(env, NUM_TENDEROS)  # Crea los recursos (peluqueros)
env.process(principal(env, personal))  # Invoca el proceso princial
env.run()  # Inicia la simulacion

print(f'El balance es de {balance}')
