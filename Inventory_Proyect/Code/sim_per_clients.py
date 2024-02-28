import random
import math
import simpy


class Simulation:
    def __init__(self, seed, NUM_TENDEROS, arrival_times, sim_time, initial_stock, STOCK_MAX, STOCK_MIN,
                 buy_price, sale_price, maintenance_cost, clients_count, Repo_Max_T, Repo_Min_T):
        self.SEMILLA = seed
        self.salesperson_count = NUM_TENDEROS
        self.arrival_time = arrival_times  # tiempo de llegada promedio entre cada cliente osea un promedio de 3 por hora
        self.sim_time = sim_time
        self.initial_stock = initial_stock
        self.STOCK_MAX = STOCK_MAX
        self.STOCK_MIN = STOCK_MIN
        self.buy_price = buy_price
        self.sale_price = sale_price
        self.maintenance_cost = maintenance_cost
        self.clients_count = clients_count
        self.Repo_Max_T = Repo_Max_T
        self.Repo_Min_T = Repo_Min_T

        self.stock = initial_stock
        self.sales_count = 0
        self.buy_to_supplier = 0
        self.money_balance = 0
        self.last_time_by_to_supplier = 0
        self.last_inventary_change = 0.0

        self.te = 0.0  # tiempo de espera total
        self.dt = 0.0  # duracion de servicio total
        self.fin = 0.0  # minuto en el que finaliza

    def need_to_buy(self) -> bool:

        if self.stock < self.STOCK_MIN:
            return True
        else:
            return False

    def restock(self, env, buy_count):

        print("Compra %.2f unidades en minuto %.2f" % (buy_count, env.now))

        R = random.random()  # Obtiene un numero aleatorio y lo guarda en R
        time = self.Repo_Max_T - self.Repo_Min_T
        buy_time = self.Repo_Min_T + (time * R)  # Distribucion uniforme
        yield env.timeout(buy_time)  # deja correr el tiempo n minutos
        self.stock += buy_count
        self.money_balance -= buy_count * self.buy_price
        self.buy_to_supplier += buy_count
        self.last_time_by_to_supplier = env.now
        print("  Compra listo en %.2f minutos tiempo actual %.2f" % (buy_time, env.now))
        # actualizar el money_balance
        self.update_balance(env)

    def atention_time(self, no_sale: bool = False):  # Distribución de probabilidad de tiempo de atención
        max_time = 5.0
        min_time = 0.7
        if no_sale == True:
            max_time = 1.0
            min_time = 0.3

        R = random.random()
        return min_time + (max_time - min_time) * R  # Distribución uniforme

    def sale_stock(self, name, env, last_sale_ok=[False]):

        buy_count = random.randint(1, 10)
        if self.stock < 1:

            time = self.atention_time(True)
            self.dt = self.dt + time
            print(f'No hay nada de stock el cliente {name} no pudo comprar {buy_count} producto')
            last_sale_ok[0] = False

            yield env.timeout(time)  # Deja correr el tiempo n minutos
        else:
            self.stock -= min(buy_count, self.stock)
            if buy_count < self.stock:
                self.money_balance += buy_count * self.sale_price
                self.sales_count += buy_count
            else:
                self.money_balance += self.stock * self.sale_price
                self.sales_count += self.stock
                self.stock = 0
            print("Venta %.2f unidades en minuto %.2f al cliente %s " % (buy_count, env.now, name))
            time = self.atention_time(no_sale=False)

            self.dt = self.dt + time
            # Fue exitosa la venta
            last_sale_ok[0] = True
            yield env.timeout(time)  # Deja correr el tiempo n minutos

    def update_balance(self, env):

        time = env.now - self.last_inventary_change
        if time > 0:
            temp = self.stock * self.maintenance_cost * time
            self.money_balance -= temp
            self.last_inventary_change = env.now
        else:
            self.last_inventary_change = env.now
        print("Balance %.2f en minuto %.2f" % (self.money_balance, env.now))

    def client(self, env, name, salesperson):

        arrival = env.now  # Guarda el minuto de llegada del cliente
        print("---> %s llego a la tienda en minuto %.2f" % (name, arrival))

        with salesperson.request() as request:  # Espera su turno
            yield request  # Obtiene turno
            pasa = env.now  # Guarda el minuto cuado comienza a ser atendido
            # hacer el análisis aca por la entrada del cliente
            self.update_balance(env)
            espera = pasa - arrival  # Calcula el tiempo que espero
            self.te = self.te + espera  # Acumula los tiempos de espera
            print("**** %s pasa con el tendero en minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
            # Vender producto
            # Si el producto Se pudo comprar se continua
            sale_bool = [False]
            yield env.process(self.sale_stock(name, env, sale_bool))  # Invoca al proceso vender
            # Actulizar el money_balance
            self.update_balance(env)
            ok_sale = sale_bool[0]
            # assert ok_sale, f"El cliente {name} no pudo comprar el producto "
            print(f"LA venta al cliente {name} fue exitosa {ok_sale}   ")
            # El cliente termina la compra
            deja = env.now
            print("<--- %s deja la tienda en minuto %.2f" % (name, deja))
            yield env.timeout(0)  # Deja correr el tiempo n minutos para poder recibir al proximo cliente

        if not ok_sale or self.need_to_buy():
            # No se pudo vender
            if not ok_sale:
                print("**** %s no se pudo vender" % name)
            # Comprar al distribuidor
            self.update_balance(env)
            yield env.process(
                self.restock(env, self.STOCK_MAX - self.stock))  # Invoca al proceso comprar al distribuidor

        self.fin = env.now  # Conserva globalmente el ultimo minuto de la simulacion

    def arrival(self, env, salesperson):
        arrival = 0
        i = 0
        for i in range(self.clients_count):  # Para n clientes
            R = random.random()
            arrival = -self.arrival_time * math.log(R)  # Distribucion exponencial
            yield env.timeout(arrival)  # Deja transcurrir un tiempo entre uno y otro

            i += 1

            env.process(self.client(env, 'Cliente %d' % i, salesperson))

    def arrival_by_time(self, env, salesperson):
        arrival = 0
        i = 0
        while env.now < self.sim_time:  # Para n clientes
            R = random.random()
            arrival = -self.arrival_time * math.log(R)  # Distribucion exponencial
            yield env.timeout(arrival)  # Deja transcurrir un tiempo entre uno y otro

            i += 1

            env.process(self.client(env, 'Cliente %d' % i, salesperson))

    def start(self, by_time: bool = True):
        print("------------------- Bienvenido Simulacion Inventario ------------------")
        random.seed(self.SEMILLA)  # Cualquier valor
        env = simpy.Environment()  # Crea el objeto entorno de simulacion
        salesperson = simpy.Resource(env, self.salesperson_count)  # Crea los recursos tendero
        if by_time:
            env.process(self.arrival_by_time(env, salesperson))
        else:
            env.process(self.arrival(env, salesperson))  # Invoca el proceso princial
        env.run()  # Inicia la simulacion

        print(f'El money_balance es de {self.money_balance}')


sim = Simulation(seed=30, sim_time=720, arrival_times=20, buy_price=200, sale_price=300, STOCK_MAX=5, STOCK_MIN=0,
                 initial_stock=1, Repo_Min_T=65, Repo_Max_T=180, NUM_TENDEROS=1, clients_count=15,
                 maintenance_cost=0.05)
sim.start()

