import random
import math
import simpy
from Utils import *


class Simulation:
    def __init__(self, seed, storekeeper, arrival_times, sim_time, initial_stock, STOCK_MAX, STOCK_MIN,
                 buy_price, sale_price, maintenance_cost, clients_count, Repo_Max_T, Repo_Min_T, min_client_order=1,
                 max_client_order=10):
        self.SEMILLA = seed
        self.salesperson_count = storekeeper
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
        # count of max and min orders by client
        self.min_client_order = min_client_order
        self.max_client_order = max_client_order

        # variables
        self.stock = initial_stock
        self.sales_count = 0
        self.buy_to_supplier = 0
        self.money_balance = 0
        self.last_time_by_to_supplier = 0
        self.last_inventary_change = 0.0

        self.te = 0.0  # tiempo de espera total
        self.dt = 0.0  # duracion de servicio total
        self.end_time = 0.0  # minuto en el que finaliza

        self.orders_count = 0
        # person
        self.people = [Person]
        # orders
        self.orders = [Orders]

        # count persons can buy

        self.count_can_by_p: int = 0

        # active order
        self.active_order = False

    def need_to_buy(self) -> bool:

        if self.stock <= self.STOCK_MIN:
            return True
        else:
            return False

    def restock(self, env, buy_count, restock_process):
        # Verifica si hay una cola antes de solicitar el recurso
        if len(restock_process.queue) > 0 or self.active_order:
            # El proceso de reabastecimiento decide abandonar
           # print(f"El proceso de reabastecimiento decidió abandonar debido a la cola.")

            return env.timeout(0)
        self.orders_count += 1
        self.active_order = True
        with restock_process.request() as request:  # Espera su turno
            yield request
            # print("Compra %.2f unidades en minuto %.2f con balance %.2f" % (buy_count, env.now, self.money_balance))

            R = random.random()  # Obtiene un numero aleatorio y lo guarda en R
            time = self.Repo_Max_T - self.Repo_Min_T
            buy_time = self.Repo_Min_T + (time * R)  # Distribucion uniforme

            b_time = env.now
            b_stock = self.stock
            yield env.timeout(buy_time)  # deja correr el tiempo n minutos
            self.stock += buy_count
            self.money_balance -= buy_count * self.buy_price
            self.buy_to_supplier += buy_count
            self.last_time_by_to_supplier = env.now

            self.orders.append(
                Orders(name=f'Compra # {self.orders_count}', count=buy_count, start_time=b_time, process_time=buy_time,
                       count_stock_before=b_stock, count_stock_after=self.stock))

            #  print("  Compra listo en %.2f minutos tiempo actual %.2f con balance %.2f" % (
            #     buy_time, env.now, self.money_balance))

            # actualizar el money_balance
            self.update_balance(env)
            self.active_order = False

    def atention_time(self, no_sale: bool = False):  # Distribución de probabilidad de tiempo de atención
        max_time = 5.0
        min_time = 0.7
        if no_sale == True:
            max_time = 1.0
            min_time = 0.3

        R = random.random()
        return min_time + (max_time - min_time) * R  # Distribución uniforme

    def count_to_buy(self):
        return random.randint(self.min_client_order, self.max_client_order)

    def sale_stock(self, name, env, index: int, last_sale_ok=[False]):
        person = self.people[index]
        # Generar variable aleatoria de cuanto comprar del producto
        buy_count = self.count_to_buy()

        person.count_to_buy = buy_count
        if self.stock < 1:
            person.can_buy = False
            time = self.atention_time(True)
            self.dt = self.dt + time
            # print(f'No hay nada de stock el cliente {name} no pudo comprar {buy_count} producto')

            last_sale_ok[0] = False
            # después de transcurrido este tiempo se va instantáneamente
            yield env.timeout(time)  # Deja correr el tiempo n minutos
        else:
            temp_count = min(buy_count, self.stock)
            self.stock -= temp_count
            self.money_balance += temp_count * self.sale_price
            self.sales_count += self.stock

            # actualizar la persona
            person.can_buy = True
            person.count_can_buy = temp_count
            self.count_can_by_p += 1

            # print("Venta %.2f unidades en minuto %.2f al cliente %s " % (buy_count, env.now, name))
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

    # print("Balance %.2f en minuto %.2f" % (self.money_balance, env.now))

    def client(self, env, name, index, salesperson, restock_process):

        arrival = env.now  # Guarda el minuto de llegada del cliente
        # print("---> %s llego a la tienda en minuto %.2f" % (name, arrival))

        with salesperson.request() as request:  # Espera su turno
            yield request  # Obtiene turno
            service_time = env.now  # Guarda el minuto cuado comienza a ser atendido
            # hacer el análisis aca por la entrada del cliente
            self.update_balance(env)
            waiting_time = service_time - arrival  # Calcula el tiempo que espero

            # actualizar la persona
            person = self.people[index]
            person.service_time = service_time
            person.waiting_time = waiting_time

            self.te = self.te + waiting_time  # Acumula los tiempos de espera
            #   print("**** %s pasa con el tendero en minuto %.2f habiendo esperado %.2f" % (
            #  name, service_time, waiting_time))
            # Vender producto
            # Si el producto Se pudo comprar se continua
            sale_bool = [False]
            yield env.process(self.sale_stock(name, env, index, sale_bool))  # Invoca al proceso vender
            # Actulizar el money_balance
            self.update_balance(env)

            #  print(f"LA venta al cliente {name} fue exitosa {ok_sale}   ")
            # El cliente termina la compra
            departure = env.now
            # actualizar la persona
            person.departure_time = departure

          #  print("<--- %s deja la tienda en minuto %.2f" % (name, departure))
            yield env.timeout(0)  # Deja correr el tiempo n minutos para poder recibir al proximo cliente

        if self.need_to_buy() and len(restock_process.queue) == 0:
            # Comprar al distribuidor
            self.update_balance(env)
            yield env.process(
                self.restock(env, self.STOCK_MAX - self.stock, restock_process))
            # Invoca al proceso comprar al distribuidor
        self.end_time = env.now  # Conserva globalmente el ultimo minuto de la simulacion

    def stop(self, env, i: int, by_time: bool):
        if by_time:
            return env.now > self.sim_time
        else:
            return i >= self.clients_count

    def arrival(self, env, salesperson, restock_process, by_time: bool = False):
        arrival = 0
        i = 0
        assert len(self.people) == 0, "La lista de personas no esta vacia"
        assert len(self.orders) == 0, "La lista de ordenes no esta vacia"
        while not self.stop(env, i, by_time):  # Para n clientes
            R = random.random()
            arrival = -self.arrival_time * math.log(R)  # Distribucion exponencial
            yield env.timeout(arrival)  # Deja transcurrir un tiempo entre uno y otro
            i += 1
            # Agregar la persona
            self.people.append(Person(name=f'Cliente {i}', arrival_time=env.now))
         #   print(f"EL CLIENTe {i} llego en el minuto {env.now}")
            env.process(self.client(env, 'Cliente %d' % i, i - 1, salesperson, restock_process))

    def arrival_by_time(self, env, salesperson, restock_process):
        arrival = 0
        i = 0
        while env.now < self.sim_time:  # Para n clientes
            R = random.random()
            arrival = -self.arrival_time * math.log(R)  # Distribucion exponencial
            yield env.timeout(arrival)  # Deja transcurrir un tiempo entre uno y otro

            i += 1

            env.process(self.client(env, 'Cliente %d' % i, i - 1, salesperson, restock_process))

    def start(self, by_time: bool = True):
        #  print("------------------- Bienvenido Simulacion Inventario ------------------")
        random.seed(self.SEMILLA)  # Cualquier valor
        env = simpy.Environment()  # Crea el objeto entorno de simulacion
        salesperson = simpy.Resource(env, self.salesperson_count)  # Crea los recursos tendero
        restock_process = simpy.Resource(env, 1)
        # limpiar las listas de personas y órdenes
        self.people = []
        self.orders = []

        env.process(self.arrival(env, salesperson, restock_process, by_time))  # Invoca el proceso princial
        env.run()  # Inicia la simulacion

        # print(f'El money_balance es de {self.money_balance}')
        result = Experiment(sim_time=self.sim_time, arrival_time=self.arrival_time, stock=self.initial_stock,
                            stock_max=self.STOCK_MAX, stock_min=self.STOCK_MIN, stock_restock=self.buy_to_supplier,
                            clients_count=self.clients_count, people=self.people, orders=self.orders,
                            money_balance=self.money_balance, service_time=self.end_time,
                            count_persons_can_buy=self.count_can_by_p)
        return result
