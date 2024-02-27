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
STOCK_MAX = 100
# cant minima de productos en stock
STOCK_MIN = 2
# precio de producto a comprar al proveedor
PRECIO_COMPRA = 200
# precio de producto a vender al cliente
PRECIO_VENTA = 300
# precio mantener una unidad de producto en stock en una unidad de tiempo
PRECIO_MANTENIMIENTO = 0.05
# Cant maxima de clientes a ver en la simulacion
TOT_CLIENTES = 3
# Tiempo Máximo en reponer
Repo_Max_T = 180
# Tiempo Minimo en reponer
Repo_Min_T = 65
# variables

# cant de productos en stock en momento i
stock = 10
# cant de productos vendidos
vendidos = 0
# cant de productos comprados al proveedor
comprados = 0
# balance dinero en caja
balance = -200
# ultimo tiempo de compra
last_time_compra = 0
# Se ultimo momento que vario la cant de inventario
last_inventary_change = 0.0
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
    #actualizar el balance
    update_balance(env)
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
    if cantidad < 1:

        time = tiempo_atención(negar=True)
        dt = dt + time

        last_sale_ok[0] = False
        yield env.timeout(time)  # Deja correr el tiempo n minutos
    else:
        stock -= min(cantidad, stock)
        if cantidad < stock:
            balance += cantidad * PRECIO_VENTA
            vendidos += cantidad
        else:
            balance += stock * PRECIO_VENTA
            vendidos += stock
            stock = 0
        print("Venta %.2f unidades en minuto %.2f al cliente %s " % (cantidad, env.now, name))
        time = tiempo_atención(negar=False)

        dt = dt + time
        # Fue exitosa la venta
        last_sale_ok[0] = True
        yield env.timeout(time)  # Deja correr el tiempo n minutos

def update_balance(env):
     global balance
     global last_inventary_change
     global stock
     global PRECIO_MANTENIMIENTO
     time=env.now-last_inventary_change
     if time>0 :
         temp=stock * PRECIO_MANTENIMIENTO*time
         balance -= temp
         last_inventary_change = env.now
     else:
            last_inventary_change = env.now
     print("Balance %.2f en minuto %.2f" % (balance, env.now))


def cliente(env, name, personal):
    global te
    global fin
    llega = env.now  # Guarda el minuto de llegada del cliente
    print("---> %s llego a la tienda en minuto %.2f" % (name, llega))

    with personal.request() as request:  # Espera su turno
        yield request  # Obtiene turno
        pasa = env.now  # Guarda el minuto cuado comienza a ser atendido
        #hacer el análisis aca por la entrada del cliente
        update_balance(env)
        espera = pasa - llega  # Calcula el tiempo que espero
        te = te + espera  # Acumula los tiempos de espera
        print("**** %s pasa con el tendero en minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
        # Vender producto
        # Si el producto Se pudo comprar se continua
        sale_bool = [False]
        yield env.process(vender(name, env, sale_bool))  # Invoca al proceso vender
         #Actulizar el balance
        update_balance(env)
        ok_sale = sale_bool[0]
        # assert ok_sale, f"El cliente {name} no pudo comprar el producto "
        print(f"LA venta al cliente {name} fue exitosa {ok_sale}    ")
        # El cliente termina la compra
        deja = env.now
        print("<--- %s deja la tienda en minuto %.2f" % (name, deja))
        yield env.timeout(0) # Deja correr el tiempo n minutos para poder recibir al proximo cliente

    if not ok_sale or hay_que_comprar():
        # No se pudo vender
        if not ok_sale:
            print("**** %s no se pudo vender" % (name))
        # Comprar al distribuidor
        update_balance(env)
        yield env.process(comprar(env, STOCK_MAX - stock))  # Invoca al proceso comprar al distribuidor


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
